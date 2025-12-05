from neo4j import GraphDatabase
import config

class Neo4jConnection:
    def __init__(self):
        # neo4j+s:// URI scheme handles SSL/TLS automatically
        # No need for additional SSL configuration
        self.driver = GraphDatabase.driver(
            config.NEO4J_URI,
            auth=(config.NEO4J_USER, config.NEO4J_PASSWORD),
            max_connection_lifetime=3600,
            keep_alive=True
        )

    def query(self, cypher, params=None):
        with self.driver.session() as session:
            result = session.run(cypher, params or {})
            return [record.data() for record in result]

neo4j = Neo4jConnection()