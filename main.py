from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import search, infobox, query_console, packages, places
import os
import uvicorn

app = FastAPI(
    title="Lancong Backend",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific frontend URL like ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allows all headers
)

app.include_router(search.router)
app.include_router(infobox.router)
app.include_router(query_console.router)
app.include_router(packages.router)
app.include_router(places.router)

@app.get("/")
def root():
    return {
        "message": "Welcome to Tourism Cuy API",
        "docs": "/docs",
        "version": "1.0.0"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/debug/config")
def debug_config():
    """Debug endpoint to check configuration (remove in production)"""
    import config
    return {
        "neo4j_uri": config.NEO4J_URI[:30] + "..." if len(config.NEO4J_URI) > 30 else config.NEO4J_URI,
        "neo4j_user": config.NEO4J_USER,
        "neo4j_password_set": bool(config.NEO4J_PASSWORD and len(config.NEO4J_PASSWORD) > 5),
        "ssl_cert_file": os.environ.get("SSL_CERT_FILE", "not set"),
        "env_check": {
            "NEO4J_URI_env": os.environ.get("NEO4J_URI", "NOT SET")[:30] + "...",
            "NEO4J_USER_env": os.environ.get("NEO4J_USER", "NOT SET"),
            "NEO4J_PASSWORD_env": "SET" if os.environ.get("NEO4J_PASSWORD") else "NOT SET"
        }
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
