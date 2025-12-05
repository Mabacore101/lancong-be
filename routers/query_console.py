from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database.neo4j_connection import neo4j

router = APIRouter(prefix="/query", tags=["QueryConsole"])

class Query(BaseModel):
    query: str

# Daftar keyword berbahaya
FORBIDDEN = [
    "delete ", "detach ", "remove ",
    "apoc.", "dbms.", "drop ", "create database"
]

@router.post("/")
def run_query(body: Query):
    cypher = body.query.strip()

    if not cypher:
        raise HTTPException(status_code=400, detail="Query tidak boleh kosong.")

    lower = cypher.lower()
    for f in FORBIDDEN:
        if f in lower:
            raise HTTPException(
                status_code=403,
                detail=f"Query terlarang demi keamanan: '{f.strip()}'"
            )

    try:
        results = neo4j.query(cypher)
        return {
            "success": True,
            "results": results
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
