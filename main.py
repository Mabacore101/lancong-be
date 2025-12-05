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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
