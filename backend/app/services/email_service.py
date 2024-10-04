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
        6. For winback campaigns:
           - Include promotional discounts for local events.
           - Make the deal very enticing to encourage the user to return to our platform.
           - Highlight what they've been missing and the value of rejoining.
        7. For weekly-digest:
           - Provide a summary of upcoming local events and activities in {user.location}.
        8. For signup-thankyou:
           - Welcome the user to the platform.
        9. Encourage user engagement and exploration of local opportunities.
        10. Mention if any of the user's followed connections are attending recommended events.
        11. Do not use any placeholders like [Your Position] or [Your Name].
        12. Do not include any greetings, introductions, or closing remarks.
        13. Start the email body directly with the main content.
        14. Do not include any sign-offs, regards, or team names at the end.
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
            r"(?i)(see you there|best regards|warm regards|regards|sincerely|thanks|cheers|best|your ai assistant),?\s*(\[\s*(your name|your title|your company|your contact information|your platform|your position|your job title|company name|platform name)\s*\])?\s*(team|organizer|company)?$",
            "",
            body.strip(),
            flags=re.IGNORECASE | re.MULTILINE,
        )

        body = re.sub(r"(?im)^.*?(regards|sincerely|thanks|cheers|best).*?$", "", body)

        body = re.sub(r"(?i)marketing officer", "", body.strip())

        body = re.sub(r"(?i)^(hi|hello|hey)\s+[^,\n]+,?\s*", "", body)

        greeting = f"Hi {user.name},\n\n"

        if email_type == "signup-thankyou":
            body = f"{greeting}Thanks for signing up for Just Friends!\n\n{body}"
            if "thanks for signing up" not in subject.lower():
                subject = "Thanks for signing up - " + subject
        elif email_type == "weekly-digest":
            body = (
                f"{greeting}Thanks for being a valuable user of Just Friends!\n\n{body}"
            )
            if "weekly digest" not in subject.lower():
                subject = "Weekly Digest - " + subject
        elif email_type == "winback":
            body = f"{greeting}{body}"
            if "welcome back" not in subject.lower():
                subject = "Welcome Back - Special Offer Inside! - " + subject

        body = re.sub(
            r"(?i)(see you there|best regards|warm regards|regards|sincerely|thanks|cheers|best|your ai assistant).*$",
            "",
            body.strip(),
        )

        body = body.strip() + common_footer

        return schemas.EmailContent(subject=subject.strip(), body=body.strip())

    except Exception as e:
        logger.error(f"Error generating email content: {str(e)}")
        raise
