from database.neo4j_connection import neo4j
from sentence_transformers import SentenceTransformer
from services.reranking_service import get_reranker
from services.wikidata import enrich_places_with_wikidata

def search_places(q: str, enrich: bool = True, max_enrich: int = 5):
    """
    Basic keyword search with optional Wikidata enrichment.
    
    Args:
        q: Search query
        enrich: Whether to enrich results with Wikidata (default: True)
        max_enrich: Maximum number of results to enrich (default: 5)
    """
    cypher = """
    MATCH (p:Place)
    WHERE toLower(p.name) CONTAINS toLower($q)
    RETURN p { .* } AS place
    LIMIT 20
    """
    results = neo4j.query(cypher, {"q": q})
    
    if not enrich or not results:
        return results
    
    # Extract places, enrich, and wrap back
    places = [r.get('place', {}) for r in results]
    enriched = enrich_places_with_wikidata(places, max_enrich)
    return [{"place": place} for place in enriched]

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def search_places_vector(q: str, top_k: int = 5, enrich: bool = True):
    """
    Semantic search with optional Wikidata enrichment.
    
    Args:
        q: Search query
        top_k: Number of results to return
        enrich: Whether to enrich results with Wikidata (default: True)
    """
    embedding = model.encode(q).tolist()

    cypher = """
    CALL db.index.vector.queryNodes(
        'place_embedding_index',
        $top_k,
        $embedding
    ) YIELD node, score
    RETURN node { .* , score: score } AS place
    """

    results = neo4j.query(cypher, {"top_k": top_k, "embedding": embedding})
    
    if not enrich or not results:
        return results
    
    # Extract places, enrich, and wrap back
    places = [r.get('place', {}) for r in results]
    enriched = enrich_places_with_wikidata(places, top_k)
    return [{"place": place} for place in enriched]

def search_places_with_reranking(q: str, initial_k: int = 20, top_k: int = 5):
    """
    Semantic search dengan reranking menggunakan cross-encoder.
    
    Workflow:
    1. Ambil initial_k kandidat menggunakan vector similarity (fast but less accurate)
    2. Rerank kandidat menggunakan cross-encoder (slower but more accurate)
    3. Return top_k hasil terbaik setelah reranking
    
    Args:
        q: Query pencarian
        initial_k: Jumlah kandidat awal dari vector search (lebih banyak = lebih baik tapi lebih lambat)
        top_k: Jumlah hasil akhir setelah reranking
    
    Returns:
        List tempat wisata yang sudah direrank berdasarkan relevance score
    """
    # Step 1: Get initial candidates using vector search
    embedding = model.encode(q).tolist()
    
    cypher = """
    CALL db.index.vector.queryNodes(
        'place_embedding_index',
        $initial_k,
        $embedding
    ) YIELD node, score
    RETURN node { .* } AS place, score AS vector_score
    """
    
    candidates = neo4j.query(cypher, {"initial_k": initial_k, "embedding": embedding})
    
    if not candidates:
        return []
    
    # Step 2: Extract places for reranking
    places_to_rerank = []
    for candidate in candidates:
        place = candidate.get('place', {})
        place['vector_score'] = candidate.get('vector_score', 0)
        places_to_rerank.append(place)
    
    # Step 3: Rerank berdasarkan name
    reranker = get_reranker()
    reranked = reranker.rerank(
        query=q,
        results=places_to_rerank,
        text_field='name',
        top_k=top_k
    )
    
    # Step 4: Enrich top results with Wikidata
    enriched = enrich_places_with_wikidata(reranked, max_enrich=top_k)
    
    # Wrap kembali dalam format yang konsisten dengan endpoint lain
    return [{"place": place} for place in enriched]

def search_places_with_advanced_reranking(
    q: str, 
    initial_k: int = 20, 
    top_k: int = 5,
    use_description: bool = True
):
    """
    Advanced semantic search dengan reranking yang mempertimbangkan deskripsi.
    Berguna untuk query yang lebih deskriptif seperti "tempat wisata alam dengan air terjun".
    
    Args:
        q: Query pencarian
        initial_k: Jumlah kandidat awal
        top_k: Jumlah hasil akhir
        use_description: Apakah menggunakan deskripsi dalam reranking
    
    Returns:
        List tempat wisata yang sudah direrank
    """
    # Get initial candidates
    embedding = model.encode(q).tolist()
    
    cypher = """
    CALL db.index.vector.queryNodes(
        'place_embedding_index',
        $initial_k,
        $embedding
    ) YIELD node, score
    RETURN node { .* } AS place, score AS vector_score
    """
    
    candidates = neo4j.query(cypher, {"initial_k": initial_k, "embedding": embedding})
    
    if not candidates:
        return []
    
    # Extract places
    places_to_rerank = []
    for candidate in candidates:
        place = candidate.get('place', {})
        place['vector_score'] = candidate.get('vector_score', 0)
        places_to_rerank.append(place)
    
    # Rerank
    reranker = get_reranker()
    
    if use_description and any('description' in p for p in places_to_rerank):
        # Use advanced reranking with description
        reranked = reranker.rerank_with_description(
            query=q,
            results=places_to_rerank,
            name_field='name',
            description_field='description',
            top_k=top_k,
            description_weight=0.3
        )
    else:
        # Fallback to simple reranking
        reranked = reranker.rerank(
            query=q,
            results=places_to_rerank,
            text_field='name',
            top_k=top_k
        )
    
    # Enrich top results with Wikidata
    enriched = enrich_places_with_wikidata(reranked, max_enrich=top_k)
    
    return [{"place": place} for place in enriched]