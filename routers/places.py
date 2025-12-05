from fastapi import APIRouter, HTTPException
from services.place_service import get_place

router = APIRouter(prefix="/places", tags=["Places"])


@router.get("/{place_id}")
def place_detail(place_id: int):
    place = get_place(place_id)
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")
    return place
