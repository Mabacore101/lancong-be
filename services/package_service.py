from database.neo4j_connection import neo4j

def get_packages():
    cypher = """
    MATCH (p:Package)
    RETURN p { .* } AS package
    """
    return neo4j.query(cypher)

def get_package_places(id: int):
    cypher = """
    MATCH (pkg:Package {id: $id})-[:INCLUDES]->(pl:Place)
    RETURN pl { .* } AS place
    """
    return neo4j.query(cypher, {"id": id})
