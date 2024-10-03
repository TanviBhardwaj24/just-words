from pydantic import BaseModel
from typing import List


class RecommendationBase(BaseModel):
    type: str
    title: str
    description: str


class Recommendation(RecommendationBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    name: str
    age: int
    location: str
    interests: List[str]


class UserWithRecommendations(BaseModel):
    id: int
    name: str
    age: int
    location: str
    interests: List[str]
    recommendations: List[Recommendation]

    class Config:
        from_attributes = True


class EmailContent(BaseModel):
    subject: str
    body: str


class EmailTypeRequest(BaseModel):
    type: str
