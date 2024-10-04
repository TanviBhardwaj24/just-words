from typing import List, Dict, Tuple
from app import schemas
from .profile_determination import determine_user_profile


def get_recommendations(
    user: schemas.UserWithRecommendations,
) -> Tuple[List[Dict], List[Dict]]:
    all_recommendations = [
        {
            "type": "event",
            "title": "Tech Startup Networking Mixer",
            "description": "Join professionals in the tech startup field",
            "location": "San Francisco",
            "date": "2024-10-15",
            "attendees": 50,
            "followed_attendees": ["John Doe", "Jane Smith"],
            "relevant_interests": ["technology", "startups", "tech startups"],
            "profile": "professional",
        },
        {
            "type": "event",
            "title": "Local Tech Meetup",
            "description": "Connect with local tech professionals and enthusiasts",
            "location": "New York",
            "date": "2024-09-05",
            "attendees": 75,
            "followed_attendees": [],
            "relevant_interests": ["technology", "networking"],
            "profile": "professional",
        },
        {
            "type": "event",
            "title": "Finance and Investment Workshop",
            "description": "Learn about local investment opportunities",
            "location": "New York",
            "date": "2024-11-05",
            "attendees": 100,
            "followed_attendees": [],
            "relevant_interests": ["finance", "investment"],
            "profile": "professional",
        },
        {
            "type": "event",
            "title": "City Photography Walk",
            "description": "Capture the essence of the city with fellow photographers",
            "location": "New York",
            "date": "2024-07-30",
            "attendees": 20,
            "followed_attendees": [],
            "relevant_interests": ["photography", "outdoors"],
            "profile": "social",
        },
        {
            "type": "event",
            "title": "Central Park Yoga Session",
            "description": "Join a relaxing yoga session in Central Park",
            "location": "New York",
            "date": "2024-08-10",
            "attendees": 30,
            "followed_attendees": [],
            "relevant_interests": ["yoga", "wellness", "outdoors"],
            "profile": "social",
        },
        {
            "type": "event",
            "title": "NYC Hiking Club Meetup",
            "description": "Explore hiking trails near New York City",
            "location": "New York",
            "date": "2024-09-20",
            "attendees": 25,
            "followed_attendees": [],
            "relevant_interests": ["hiking", "outdoors"],
            "profile": "social",
        },
        {
            "type": "event",
            "title": "Surf's Up: Beach Day",
            "description": "Join fellow surf enthusiasts for a day at the beach",
            "location": "San Francisco",
            "date": "2024-07-25",
            "attendees": 40,
            "followed_attendees": [],
            "relevant_interests": ["surfing", "outdoors"],
            "profile": "social",
        },
        {
            "type": "event",
            "title": "Startup Pitch Night",
            "description": "Watch and network with innovative startups pitching their ideas",
            "location": "San Francisco",
            "date": "2024-08-18",
            "attendees": 150,
            "followed_attendees": [],
            "relevant_interests": ["startups", "technology", "networking"],
            "profile": "professional",
        },
        {
            "type": "event",
            "title": "Culinary Workshop: Farm to Table",
            "description": "Learn to cook with fresh, local ingredients",
            "location": "New York",
            "date": "2024-09-12",
            "attendees": 15,
            "followed_attendees": [],
            "relevant_interests": ["cooking", "food"],
            "profile": "social",
        },
        {
            "type": "event",
            "title": "Marathon Training Group",
            "description": "Join fellow runners preparing for the upcoming city marathon",
            "location": "New York",
            "date": "2024-08-05",
            "attendees": 30,
            "followed_attendees": [],
            "relevant_interests": ["running", "fitness"],
            "profile": "social",
        },
        {
            "type": "event",
            "title": "Acting Workshop: Improv Techniques",
            "description": "Enhance your acting skills with improv exercises",
            "location": "Los Angeles",
            "date": "2024-10-08",
            "attendees": 20,
            "followed_attendees": [],
            "relevant_interests": ["acting", "performance"],
            "profile": "social",
        },
        {
            "type": "event",
            "title": "Ballet Master Class",
            "description": "Learn from professional ballet dancers in this intensive workshop",
            "location": "New York",
            "date": "2024-11-15",
            "attendees": 25,
            "followed_attendees": [],
            "relevant_interests": ["ballet", "dance"],
            "profile": "social",
        },
    ]

    user_profile = determine_user_profile(user)
    user_interests = [interest.lower() for interest in (user.interests or [])]
    user_location = user.location.lower()

    # Filter recommendations based on user location and interests
    local_recommendations = [
        rec
        for rec in all_recommendations
        if rec["location"].lower() == user_location
        and any(
            interest in user_interests for interest in rec.get("relevant_interests", [])
        )
    ]

    if not local_recommendations:
        local_recommendations = [
            rec
            for rec in all_recommendations
            if any(
                interest in user_interests
                for interest in rec.get("relevant_interests", [])
            )
        ]

    if not local_recommendations:
        local_recommendations = [
            rec
            for rec in all_recommendations
            if rec["location"].lower() == user_location
        ]

    if not local_recommendations:
        local_recommendations = all_recommendations

    primary_recommendations = [
        rec for rec in local_recommendations if rec["profile"] == user_profile
    ]
    secondary_recommendations = [
        rec for rec in local_recommendations if rec["profile"] != user_profile
    ]

    if not primary_recommendations:
        primary_recommendations, secondary_recommendations = (
            secondary_recommendations[:2],
            secondary_recommendations[2:],
        )
    if not secondary_recommendations:
        secondary_recommendations = primary_recommendations[-2:]
        primary_recommendations = primary_recommendations[:-2]

    primary_recommendations.sort(key=lambda x: x["date"])
    secondary_recommendations.sort(key=lambda x: x["date"])

    return primary_recommendations, secondary_recommendations
