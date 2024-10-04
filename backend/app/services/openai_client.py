import os
import logging
from openai import OpenAI
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
