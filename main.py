from fastapi import FastAPI
from routers import search, infobox, query_console, packages

app = FastAPI(
    title="Tourism Cuy KG Backend",
    version="1.0.0",
)

app.include_router(search.router)
app.include_router(infobox.router)
app.include_router(query_console.router)
app.include_router(packages.router)
