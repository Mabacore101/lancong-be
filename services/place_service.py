from database.neo4j_connection import neo4j

def get_place_by_id(id: int):
    cypher = """
    MATCH (p:Place {id: $id})
    RETURN p { .* } AS place
    """
    res = neo4j.query(cypher, {"id": id})
    return res[0] if res else {}