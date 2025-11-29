from fastapi import APIRouter
from services.search_service import search_places

router = APIRouter(prefix="/search", tags=["Search"])

@router.get("/")
def search(query: str):
    return search_places(query)