from fastapi import APIRouter, Query
from services.search_service import (
    search_places, 
    search_places_vector,
    search_places_with_reranking,
    search_places_with_advanced_reranking
)

router = APIRouter(prefix="/search", tags=["Search"])

@router.get("/")
def search(query: str):
    """
    Basic keyword search - mencari tempat wisata berdasarkan nama.
    Paling cepat tapi paling sederhana.
    """
    return search_places(query)

@router.get("/ai")
def search_ai(query: str, k: int = 5):
    """
    Semantic search menggunakan vector embeddings.
    Lebih pintar dari keyword search, bisa menangkap semantic similarity.
    """
    return search_places_vector(query, k)

@router.get("/rerank")
def search_with_rerank(
    query: str,
    initial_k: int = Query(default=20, description="Jumlah kandidat awal dari vector search"),
    top_k: int = Query(default=5, description="Jumlah hasil akhir setelah reranking")
):
    """
    Semantic search + Reranking menggunakan cross-encoder.
    
    Workflow:
    1. Ambil 'initial_k' kandidat menggunakan vector similarity (cepat)
    2. Rerank kandidat menggunakan cross-encoder model (akurat)
    3. Return 'top_k' hasil terbaik
    
    Paling akurat untuk mencari relevansi hasil pencarian.
    Lebih lambat dari /ai tapi lebih presisi.
    """
    return search_places_with_reranking(query, initial_k, top_k)

@router.get("/rerank-advanced")
def search_with_advanced_rerank(
    query: str,
    initial_k: int = Query(default=20, description="Jumlah kandidat awal dari vector search"),
    top_k: int = Query(default=5, description="Jumlah hasil akhir setelah reranking"),
    use_description: bool = Query(default=True, description="Gunakan deskripsi dalam reranking")
):
    """
    Advanced semantic search + Reranking dengan mempertimbangkan deskripsi.
    
    Berguna untuk query yang lebih deskriptif, misalnya:
    - "tempat wisata alam dengan air terjun"
    - "pantai yang bagus untuk snorkeling"
    - "museum sejarah di Jakarta"
    
    Akan mencocokkan query dengan nama DAN deskripsi tempat wisata.
    Paling lambat tapi paling pintar untuk query deskriptif.
    """
    return search_places_with_advanced_reranking(query, initial_k, top_k, use_description)