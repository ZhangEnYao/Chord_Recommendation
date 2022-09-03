from fastapi import APIRouter
from . import chord_recommendation_router

router = APIRouter()
router.include_router(chord_recommendation_router.router, prefix = '/ChordRecommendation')