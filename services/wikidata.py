from SPARQLWrapper import SPARQLWrapper, JSON

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
