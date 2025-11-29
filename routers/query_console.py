from fastapi import APIRouter
from pydantic import BaseModel
from database.neo4j_connection import neo4j

router = APIRouter(prefix="/query", tags=["QueryConsole"])

class Query(BaseModel):
    cypher: str

@router.post("/")
def run_query(body: Query):
    try:
        return neo4j.query(body.cypher)
    except Exception as e:
        return {"error": str(e)}
