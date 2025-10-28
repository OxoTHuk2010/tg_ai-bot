import json
import re
from typing import List, Dict, Optional
from openai import AsyncOpenAI, APITimeoutError, APIConnectionError, RateLimitError, APIError
from config import OpenAI_KEY

client = AsyncOpenAI(api_key=OpenAI_KEY)

_SCHEMA_HINT = (
    'Верни строго JSON по схеме: '
    '{"items":[{"title":"<название>","why":"<1-2 предложения описания>"}]} '
    'Без пояснений и без кодовых блоков.'
)

def _strip_code_fences(s: str) -> str:
    s = (s or "").strip()
    if s.startswith("```"):
        s = re.sub(r"^```(?:json)?\s*|\s*```$", "", s, flags=re.S)
    return s.strip()

def _extract_first_json_object(s: str) -> Optional[str]:
    s = s or ""
    start = s.find("{")
    end = s.rfind("}")
    if start != -1 and end != -1 and end > start:
        return s[start:end+1]
    return None

def _normalize_items(raw_items: List[dict]) -> List[Dict[str, str]]:
    out: List[Dict[str, str]] = []
    for it in (raw_items or [])[:5]:
        title = str(it.get("title", "")).strip()
        why = str(it.get("why", "")).strip()
        if title:
            out.append({"title": title, "why": why})
    return out[:5]

def _get_items_field(data: dict) -> List[dict]:
    return data.get("items") or data.get("item") or data.get("recommendations") or []

def _safe_json_parse(raw: str) -> Optional[dict]:
    """
    Пытаемся распарсить JSON:
    1) как есть
    2) убрав кодфенсы
    3) вытащив первый JSON-объект из текста
    """
    if not raw or not raw.strip():
        return None
    # попыка №1 — как есть
    try:
        return json.loads(raw)
    except Exception:
        pass
    # попытка №2 — снять кодфенсы
    cleaned = _strip_code_fences(raw)
    if cleaned != raw:
        try:
            return json.loads(cleaned)
        except Exception:
            pass
    # попытка №3 — вытащить {…}
    only_obj = _extract_first_json_object(cleaned)
    if only_obj:
        try:
            return json.loads(only_obj)
        except Exception:
            pass
    return None

async def _ask_json_mode(category: str, genre: str, blacklist: List[str]) -> List[Dict[str, str]]:
    bl = ", ".join(blacklist) if blacklist else "—"
    prompt = (
        f"Категория: {category}\nЖанр: {genre}\nНе предлагать: {bl}\n"
        f"Дай ровно 5 рекомендаций.\n{_SCHEMA_HINT}"
    )
    resp = await client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "Ты даёшь точные медиа-рекомендации на русском языке."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        max_tokens=900,
    )
    raw = (resp.choices[0].message.content or "").strip()
    data = _safe_json_parse(raw)
    if not data:
        return []
    return _normalize_items(_get_items_field(data))

async def _ask_json_loose(category: str, genre: str, blacklist: List[str]) -> List[Dict[str, str]]:
    bl = ", ".join(blacklist) if blacklist else "—"
    prompt = (
        f"Категория: {category}\nЖанр: {genre}\nНе предлагать: {bl}\n{_SCHEMA_HINT}"
    )
    resp = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Ты даёшь точные медиа-рекомендации на русском языке."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        max_tokens=900,
    )
    raw = (resp.choices[0].message.content or "").strip()
    data = _safe_json_parse(raw)
    if not data:
        return []
    return _normalize_items(_get_items_field(data))

async def _ask_text_list(category: str, genre: str, blacklist: List[str]) -> List[Dict[str, str]]:
    bl = ", ".join(blacklist) if blacklist else "—"
    prompt = (
        f"Категория: {category}\nЖанр: {genre}\nНе предлагать: {bl}\n"
        "Дай 5 пунктов в формате:\n"
        "1) Название — 1-2 предложения пояснения\n"
        "2) ...\n"
        "Только список, без лишнего текста."
    )
    resp = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=700,
    )
    txt = (resp.choices[0].message.content or "").strip()
    items: List[Dict[str, str]] = []
    for m in re.finditer(r"^\s*\d+[\).]\s*(.+?)\s*—\s*(.+)$", txt, flags=re.M):
        title = m.group(1).strip()
        why = m.group(2).strip()
        if title:
            items.append({"title": title, "why": why})
        if len(items) == 5:
            break
    return items

async def get_recommendations_structured(category: str, genre: str, blacklist: List[str]) -> List[Dict[str, str]]:

    try:
        items = await _ask_json_mode(category, genre, blacklist)
        if items:
            return items
        items = await _ask_json_loose(category, genre, blacklist)
        if items:
            return items
        items = await _ask_text_list(category, genre, blacklist)
        return items
    except (APITimeoutError, APIConnectionError, RateLimitError, APIError):
        return []
    except Exception:
        return []
