from pydantic import BaseModel

class Place(BaseModel):
    id: int
    name: str
    city: str | None = None
    category: str | None = None
    rating: float | None = None
