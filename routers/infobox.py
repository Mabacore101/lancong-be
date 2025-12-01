from fastapi import APIRouter
from services.infobox_service import get_infobox

router = APIRouter(prefix="/infobox", tags=["Infobox"])

@router.get("/{place_id}")
def infobox(place_id: int):
    data = get_infobox(place_id)
    if data is None:
        return {"error": "Place not found"}
    return data
