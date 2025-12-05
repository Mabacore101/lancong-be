from SPARQLWrapper import SPARQLWrapper, JSON
from typing import Dict, Any, List

def fetch_wikidata_image(place_name: str):
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    
    query = f"""
    PREFIX wdt: <http://www.wikidata.org/prop/direct/>
    PREFIX schema: <http://schema.org/>
    PREFIX wikibase: <http://wikiba.se/ontology#>
    PREFIX bd: <http://www.bigdata.com/rdf#>
    PREFIX mwapi: <https://www.mediawiki.org/ontology#API/>

    SELECT ?item ?itemLabel ?image ?description WHERE {{
      SERVICE wikibase:mwapi {{
          bd:serviceParam wikibase:endpoint "www.wikidata.org";
                          wikibase:api "EntitySearch";
                          mwapi:search "{place_name}";
                          mwapi:language "id".
          ?item wikibase:apiOutputItem mwapi:item.
      }}

      OPTIONAL {{ ?item wdt:P18 ?image. }}

      OPTIONAL {{ 
        ?item schema:description ?description. 
        FILTER(LANG(?description) = "id") 
      }}

      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "id". }}
    }}
    LIMIT 1
    """

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    try:
        results = sparql.query().convert()
        bindings = results["results"]["bindings"]
        if len(bindings) > 0:
            item = bindings[0]
            return {
                "image": item.get("image", {}).get("value"),
                "wikidata_entity": item.get("item", {}).get("value"),
                "description_id": item.get("description", {}).get("value")
            }
    except:
        return None
    return None


def enrich_place_with_wikidata(place: Dict[str, Any]) -> Dict[str, Any]:
    """
    Enrich a single place object with Wikidata information.
    
    Args:
        place: Place dictionary containing at least 'name' field
        
    Returns:
        Place dictionary enriched with image, wikidata_entity, and description_id
    """
    external = fetch_wikidata_image(place.get("name", ""))
    if external:
        place["image"] = external.get("image")
        place["wikidata_entity"] = external.get("wikidata_entity")
        place["description_id"] = external.get("description_id")
    else:
        place["image"] = None
        place["wikidata_entity"] = None
        place["description_id"] = None
    
    return place


def enrich_places_with_wikidata(places: List[Dict[str, Any]], max_enrich: int = 5) -> List[Dict[str, Any]]:
    """
    Enrich multiple place objects with Wikidata information.
    Only enriches the first 'max_enrich' places to avoid slow response times.
    
    Args:
        places: List of place dictionaries
        max_enrich: Maximum number of places to enrich (default: 5)
        
    Returns:
        List of places with top results enriched with Wikidata info
    """
    enriched_places = []
    
    for i, place in enumerate(places):
        if i < max_enrich:
            # Enrich top results with Wikidata
            enriched_places.append(enrich_place_with_wikidata(place))
        else:
            # Don't enrich remaining results (performance optimization)
            place["image"] = None
            place["wikidata_entity"] = None
            place["description_id"] = None
            enriched_places.append(place)
    
    return enriched_places
