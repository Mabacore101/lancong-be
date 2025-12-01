from database.neo4j_connection import neo4j
from services.wikidata import fetch_wikidata_image

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

    external = fetch_wikidata_image(info["name"])
    if external:
        info["image"] = external.get("image")
        info["wikidata_entity"] = external.get("wikidata_entity")
        info["description_id"] = external.get("description_id")
    else:
        info["image"] = None
        info["wikidata_entity"] = None
        info["description_id"] = None

    return info
