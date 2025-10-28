from aiogram import Router
from .commands_handlers import router as commands_router
from .callbacks_handler import router as callbacks_router
from .states_handler import router as state_router
from .translate_handlers import router as translate_router
from .reco_handlers import router as reco_router
from .resume_handlers import router as resume_router

router = Router()
router.include_routers(
    commands_router,
    callbacks_router,
    state_router,
    translate_router,
    reco_router,
    resume_router,
)