from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

# Dummy data
users = {
    "1": {"id": "1", "name": "Tanvi", "interests": ["web-dev", "hiking", "running"]},
    "2": {"id": "2", "name": "Jane", "interests": ["marketing", "dancing", "yoga"]},
}

class User(BaseModel):
    id: str
    name: str
    interests: List[str]

class Recommendation(BaseModel):
    type: str
    title: str
    description: str

class EmailContent(BaseModel):
    subject: str
    body: str

@app.get("/api/users/{user_id}", response_model=User)
async def get_user(user_id: str):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    return users[user_id]

@app.get("/api/recommendations/{user_id}", response_model=List[Recommendation])
async def get_recommendations(user_id: str):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Dummy recommendation logic
    user = users[user_id]
    recommendations = [
        Recommendation(type="event", title="Tech Meetup", description="Join fellow tech enthusiasts!"),
        Recommendation(type="job", title="Software Developer", description="Exciting opportunity at XYZ Corp"),
    ]
    return recommendations

@app.post("/api/generate-email/{user_id}", response_model=EmailContent)
async def generate_email(user_id: str):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    
    user = users[user_id]
    recommendations = await get_recommendations(user_id)
    
    # Dummy email generation logic
    subject = f"Personalized Recommendations for {user['name']}"
    body = f"Hello {user['name']},\n\nBased on your interests in {', '.join(user['interests'])}, we thought you might like:\n\n"
    for rec in recommendations:
        body += f"- {rec.title}: {rec.description}\n"
    body += "\nBest regards,\nYour Marketing Team"
    
    return EmailContent(subject=subject, body=body)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
