import logging
from app import schemas
from .profile_determination import determine_user_profile
from .email_service import generate_email_content
from .recommendation_service import get_recommendations
from .openai_client import get_openai_client

logger = logging.getLogger(__name__)

try:
    client = get_openai_client()
except ValueError as e:
    logger.error(f"Failed to initialize OpenAI client: {str(e)}")
    client = None


def generate_personalized_email(
    user: schemas.UserWithRecommendations, email_type: str
) -> schemas.EmailContent:
    try:
        user_profile = determine_user_profile(user)
        logger.info(f"Determined user profile: {user_profile}")

        primary_recommendations, secondary_recommendations = get_recommendations(user)

        email_content = generate_email_content(
            user,
            email_type,
            user_profile,
            primary_recommendations,
            secondary_recommendations,
        )

        return email_content

    except Exception as e:
        logger.error(f"Error in generate_personalized_email: {str(e)}")
        raise
