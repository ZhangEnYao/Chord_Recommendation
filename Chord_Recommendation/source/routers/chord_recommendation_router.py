from fastapi import APIRouter
from ..application import application_main

router = APIRouter()
@router.get('/ShowFingerBoard:Chord={chord},Mode={mode}')
async def show_fingerboard(chord, mode):
    application_main.ShowFingerBoard(chord, mode)
    return 'Success'