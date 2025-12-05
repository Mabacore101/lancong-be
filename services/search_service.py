from database.neo4j_connection import neo4j
from sentence_transformers import SentenceTransformer

def search_places(q: str):
    cypher = """
    MATCH (p:Place)
    WHERE toLower(p.name) CONTAINS toLower($q)
    RETURN p { .* } AS place
    LIMIT 20
    """
    return neo4j.query(cypher, {"q": q})

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
def search_places_vector(q: str, top_k: int = 5):
    embedding = model.encode(q).tolist()

    cypher = """
    CALL db.index.vector.queryNodes(
        'place_embedding_index',
        $top_k,
        $embedding
    ) YIELD node, score
    RETURN node { .* , score: score } AS place
    """

    return neo4j.query(cypher, {"top_k": top_k, "embedding": embedding})