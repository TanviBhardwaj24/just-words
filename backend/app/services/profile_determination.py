from app import schemas


def determine_user_profile(user: schemas.UserWithRecommendations) -> str:
    professional_keywords = [
        "professional",
        "networking",
        "career",
        "business",
        "industry",
        "work",
        "job",
        "opportunity",
        "startup",
    ]
    social_keywords = [
        "social",
        "friends",
        "community",
        "fun",
        "hobby",
        "interests",
        "activities",
        "events",
    ]

    text = f"{user.description or ''} {' '.join(user.interests or [])}".lower()

    professional_count = sum(text.count(kw) for kw in professional_keywords)
    social_count = sum(text.count(kw) for kw in social_keywords)

    print(f"Professional count: {professional_count}, Social count: {social_count}")

    if professional_count > social_count:
        return "professional"
    elif social_count > professional_count:
        return "social"
    else:
        return "general"
