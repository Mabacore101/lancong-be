from fastapi import APIRouter
from services.search_service import search_places, search_places_vector

router = APIRouter(prefix="/search", tags=["Search"])

@router.get("/")
def search(query: str):
    return search_places(query)

@router.get("/ai")
def search_ai(query: str, k: int = 5):
    return search_places_vector(query, k)