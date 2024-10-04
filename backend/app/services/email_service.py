import re
import logging
from app import schemas
from .openai_client import client
from .formatter import format_recommendations

logger = logging.getLogger(__name__)


def generate_email_content(
    user: schemas.UserWithRecommendations,
    email_type: str,
    user_profile: str,
    primary_recommendations: list,
    secondary_recommendations: list,
) -> schemas.EmailContent:
    if client is None:
        raise RuntimeError(
            "OpenAI client is not initialized. Check your API key configuration."
        )

    try:
        common_footer = "\n\nBest Regards,\nJust Friends Team"

        prompt = f"""
        Generate a personalized email for a user with the following details:
        Name: {user.name}
        Age: {user.age}
        Location: {user.location}
        Interests: {', '.join(user.interests or [])}
        Description: {user.description}
        Profile: {user_profile}

        Primary Recommendations (Events most relevant to the user's profile):
        {format_recommendations(primary_recommendations)}

        Secondary Recommendations (Other local events that might interest the user):
        {format_recommendations(secondary_recommendations)}

        Email Type: {email_type}

        The email should:
        1. Be tailored to the user's profile ({user_profile}), interests, and location ({user.location}).
        2. Have a tone appropriate for the user's profile and email type.
        3. Emphasize that all recommendations are local events in or near {user.location}.
        4. Highlight how the primary recommendations align with the user's main interests or profile.
        5. Present secondary recommendations as additional options that might broaden the user's interests.
        6. For winback campaigns, include promotional discounts for local events if available.
        7. For weekly digests, provide a summary of upcoming local events and activities.
        8. Encourage user engagement and exploration of local opportunities.
        9. Mention if any of the user's followed connections are attending recommended events.
        10. Do not use any placeholders like [Your Position] or [Your Name].
        11. Do not sign the email as "Marketing Officer" or any other title.

        Format the response as:
        Subject: [Email Subject]

        [Email Body]
        """

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI assistant creating personalized email content.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=500,
            n=1,
            temperature=0.7,
        )

        generated_text = response.choices[0].message.content.strip()
        subject, body = generated_text.split("\n\n", 1)

        subject = re.sub(r"^Subject:\s*", "", subject).strip()

        body = re.sub(
            r"(?i)(best regards|warm regards|regards|sincerely|thanks|cheers),?\s*(\[\s*(your name|your title|your company|your contact information|your platform|your position|your job title|company name|platform name)\s*\])?\s*(team|organizer|company)?",
            "",
            body.strip(),
            flags=re.IGNORECASE,
        )

        body = re.sub(r"(?i)marketing officer", "", body.strip())

        body = body.strip() + common_footer

        return schemas.EmailContent(subject=subject.strip(), body=body.strip())

    except Exception as e:
        logger.error(f"Error generating email content: {str(e)}")
        raise
