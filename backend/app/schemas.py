from pydantic import BaseModel
from typing import List, Optional


class RecommendationBase(BaseModel):
    type: str
    title: str
    description: str


class Recommendation(RecommendationBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True


class UserWithRecommendations(BaseModel):
    id: int
    name: str
    age: int
    location: str
    interests: List[str]
    recommendations: List[Recommendation]
    facebook: Optional[str] = None
    instagram: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    description: Optional[str] = None
    follows: Optional[List[str]] = []

    class Config:
        from_attributes = True


class EmailContent(BaseModel):
    subject: str
    body: str


class EmailTypeRequest(BaseModel):
    type: str
