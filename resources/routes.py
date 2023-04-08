from fastapi import APIRouter
from resources.rates import router as rates_router
from resources.actions import router as action_router

api_router = APIRouter()
api_router.include_router(rates_router)
api_router.include_router(action_router)