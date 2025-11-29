from fastapi import APIRouter
from services.place_service import get_place_by_id

router = APIRouter(prefix="/infobox", tags=["InfoBox"])

@router.get("/{place_id}")
def get_place(place_id: int):
    return get_place_by_id(place_id)
