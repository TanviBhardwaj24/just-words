from openai import OpenAI
import os
import logging
from app import schemas
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
load_dotenv()


def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OpenAI API key is not set. Please set the OPENAI_API_KEY environment variable."
        )
    return OpenAI(api_key=api_key)


try:
    client = get_openai_client()
except ValueError as e:
    logger.error(f"Failed to initialize OpenAI client: {str(e)}")
    client = None


def generate_email_content(
    user: schemas.UserWithRecommendations,
) -> schemas.EmailContent:
    if client is None:
        raise RuntimeError(
            "OpenAI client is not initialized. Check your API key configuration."
        )

    try:
        prompt = f"""
        Generate a personalized email for a user with the following details:
        Name: {user.name}
        Age: {user.age}
        Location: {user.location}
        Interests: {', '.join(user.interests)}

        Recommendations:
        {' '.join([f"- {rec.title}: {rec.description}" for rec in user.recommendations])}

        The email should:
        1. Be friendly and personalized
        2. Mention the user's interests
        3. Highlight the recommendations
        4. Encourage the user to explore the platform further

        Format the response as:
        Subject: [Generated Subject]

        [Generated Email Body]
        """

        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=500,
            n=1,
            stop=None,
            temperature=0.7,
        )

        generated_text = response.choices[0].text.strip()
        subject, body = generated_text.split("\n\n", 1)

        return schemas.EmailContent(subject=subject.replace("Subject: ", ""), body=body)
    except Exception as e:
        logger.error(f"Error in LLM service: {str(e)}")
        raise
