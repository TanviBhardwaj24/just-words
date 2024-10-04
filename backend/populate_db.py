from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import UserModel, RecommendationModel, FollowModel
from app.database import Base
import os
import random
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_social_links():
    username = "".join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=8))
    return {
        "facebook": f"https://www.facebook.com/{username}",
        "instagram": f"https://www.instagram.com/{username}",
        "linkedin": f"https://www.linkedin.com/in/{username}",
        "github": f"https://github.com/{username}",
    }


def generate_description(user):
    networking_keywords = ["tech", "startups", "business", "finance", "networking"]
    social_keywords = ["yoga", "surfing", "hiking", "photography", "cooking", "running"]

    interests = ", ".join(user["interests"])

    if any(kw in user["interests"] for kw in networking_keywords):
        return (
            f"Hi, I'm {user['name']}! I'm based in {user['location']} and I'm really into {interests}. "
            "I enjoy connecting with people in my field and would love to meet others who share similar professional interests. "
            "Looking forward to building meaningful connections!"
        )

    elif any(kw in user["interests"] for kw in social_keywords):
        return (
            f"Hey there! I'm {user['name']} from {user['location']}. I love spending my time doing {interests}, "
            "and I'm always excited to meet new people who share the same hobbies. "
            "Let's connect and explore new activities together!"
        )

    else:
        return (
            f"Hi, I'm {user['name']} and I'm from {user['location']}. I’m interested in {interests} "
            "and always up for meeting new people. I'm looking forward to discovering new connections who have similar interests!"
        )


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
        "name": "Sophia Martinez",
        "age": 31,
        "location": "New York",
        "profession": "Theatre",
        "interests": ["acting", "ballet", "literature"],
        "recommendations": [
            {
                "type": "event",
                "title": "Broadway Play",
                "description": "Catch a thrilling new performance on Broadway!",
            },
            {
                "type": "activity",
                "title": "Acting Workshop",
                "description": "Join an immersive acting workshop for professionals.",
            },
        ],
    },
    {
        "name": "Ethan Johnson",
        "age": 29,
        "location": "San Francisco",
        "profession": "Sales",
        "interests": ["tech startups", "cycling", "photography"],
        "recommendations": [
            {
                "type": "event",
                "title": "Sales Networking Event",
                "description": "Connect with other sales professionals in the tech industry.",
            },
            {
                "type": "activity",
                "title": "Golden Gate Park Cycling",
                "description": "Enjoy a scenic ride through Golden Gate Park.",
            },
        ],
    },
]

try:
    user_objs = []
    for user_data in users:
        social_links = generate_social_links()

        description = generate_description(user_data)

        user = UserModel(
            name=user_data["name"],
            age=user_data["age"],
            location=user_data["location"],
            interests=user_data["interests"],
            facebook=social_links["facebook"],
            instagram=social_links["instagram"],
            linkedin=social_links["linkedin"],
            github=social_links["github"],
            description=description,
        )
        db.add(user)
        db.flush()
        user_objs.append(user)

        logger.info(f"Added user: {user.name} with id: {user.id}")

        for rec_data in user_data["recommendations"]:
            recommendation = RecommendationModel(
                user_id=user.id,
                type=rec_data["type"],
                title=rec_data["title"],
                description=rec_data["description"],
            )
            db.add(recommendation)
            db.flush()
            logger.info(f"Added recommendation for user {user.id}: {rec_data['title']}")

    for user in user_objs:
        potential_follows = [u for u in user_objs if u.id != user.id]
        num_follows = random.randint(1, len(potential_follows))
        followed_users = random.sample(potential_follows, num_follows)

        for followed_user in followed_users:
            follow = FollowModel(from_user_id=user.id, to_user_id=followed_user.id)
            db.add(follow)
            logger.info(f"{user.name} is now following {followed_user.name}")

    db.commit()
    logger.info("All data committed successfully")
except Exception as e:
    db.rollback()
    logger.error(f"An error occurred: {str(e)}")
finally:
    db.close()

print("Database population script completed.")
