from fastapi import APIRouter
from ..application import application_main

router = APIRouter()
@router.get('/ShowChordCompositions:Chord={chord}')
async def get_chord_recommendation(chord):
    return str(application_main.ShowChordCompositions(chord))

@router.get('/ShowFingerBoard')
async def show_fingerboard():
    application_main.ShowFingerBoard()
    return 'Success'