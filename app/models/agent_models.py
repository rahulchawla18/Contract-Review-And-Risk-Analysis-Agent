from pydantic import BaseModel


class ReviewResponse(BaseModel):
    clauses: dict
    risks: dict
    suggestions: str