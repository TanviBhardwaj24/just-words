from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import UserModel, RecommendationModel  # Correct import
from app.database import Base  # Base should come from app.database, not app.main
import os

SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://justwords_user:password@localhost:5432/emailrecommendations",
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

db = SessionLocal()

users = [
    {
        "name": "Tanvi Bhardwaj",
        "age": 28,
        "location": "New York",
        "interests": ["technology", "hiking", "photography"],
        "recommendations": [
            {
                "type": "event",
                "title": "Tech Meetup",
                "description": "Join fellow tech enthusiasts in New York!",
            },
            {
                "type": "activity",
                "title": "Weekend Hike",
                "description": "Explore the beautiful trails near New York.",
            },
        ],
    },
    {
        "name": "Jane Doe",
        "age": 35,
        "location": "San Francisco",
        "interests": ["startups", "surfing", "yoga"],
        "recommendations": [
            {
                "type": "job",
                "title": "Startup Fair",
                "description": "Connect with innovative startups in San Francisco.",
            },
            {
                "type": "event",
                "title": "Beach Yoga Session",
                "description": "Join us for a relaxing yoga session by the ocean.",
            },
        ],
    },
    {
        "name": "John Smith",
        "age": 42,
        "location": "Chicago",
        "interests": ["finance", "running", "cooking"],
        "recommendations": [
            {
                "type": "event",
                "title": "Financial Workshop",
                "description": "Learn about personal finance and investing strategies.",
            },
            {
                "type": "activity",
                "title": "City Marathon",
                "description": "Participate in the annual Chicago Marathon!",
            },
        ],
    },
]

for user_data in users:
    user = UserModel(
        name=user_data["name"],
        age=user_data["age"],
        location=user_data["location"],
        interests=user_data["interests"],
    )
    db.add(user)
    db.flush()

    for rec_data in user_data["recommendations"]:
        recommendation = RecommendationModel(
            user_id=user.id,
            type=rec_data["type"],
            title=rec_data["title"],
            description=rec_data["description"],
        )
        db.add(recommendation)

# Commit the changes
db.commit()

# Close the session
db.close()

print("Database populated with sample data!")
