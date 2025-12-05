from database.neo4j_connection import neo4j
from services.wikidata import fetch_wikidata_image, enrich_place_with_wikidata

def get_infobox(place_id: int):

    cypher = """
    MATCH (p:Place {id: $id})
    RETURN {
        id: p.id,
        name: p.name,
        description: p.description,
        category: p.category,
        city: p.city,
        price: p.price,
        rating: p.rating,
        time_minutes: p.time_minutes,
        lat: p.lat,
        long: p.long
    } AS info
    """

    result = neo4j.query(cypher, {"id": place_id})

    if not result:
        return None

    info = result[0]["info"]
    
    # Enrich with Wikidata
    return enrich_place_with_wikidata(info)
