from database.neo4j_connection import neo4j

def search_places(q: str):
    cypher = """
    MATCH (p:Place)
    WHERE toLower(p.name) CONTAINS toLower($q)
    RETURN p { .* } AS place
    LIMIT 20
    """
    return neo4j.query(cypher, {"q": q})