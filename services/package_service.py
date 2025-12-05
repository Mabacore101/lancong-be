from database.neo4j_connection import neo4j

def get_package(package_id: int):
    cypher = """
    MATCH (pkg:Package {id: $id})
    OPTIONAL MATCH (pkg)-[:INCLUDES]->(p:Place)
    WITH pkg, collect({
        id: p.id,
        name: p.name,
        category: p.category,
        rating: p.rating
    }) AS places
    RETURN {
        id: pkg.id,
        city: pkg.city,
        places: places
    } AS package
    """
    result = neo4j.query(cypher, {"id": package_id})
    return result[0]["package"] if result else None



def get_packages(limit: int):
    cypher = """
    MATCH (pkg:Package)
    RETURN {
        id: pkg.id,
        city: pkg.city
    } AS package
    LIMIT $limit
    """
    result = neo4j.query(cypher, {"limit": limit})
    return [row["package"] for row in result]

