from database.neo4j_connection import neo4j

def get_place(place_id: int):
    cypher = """
    MATCH (p:Place {id: $id})
    RETURN {
        id: p.id,
        name: p.name,
        city: p.city,
        category: p.category,
        rating: p.rating,
        price: p.price,
        lat: p.lat,
        long: p.long
    } AS place
    """
    result = neo4j.query(cypher, {"id": place_id})
    return result[0]["place"] if result else None
