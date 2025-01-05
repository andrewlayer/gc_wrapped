import os
from openai import OpenAI


openai_client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY", None),
    base_url=os.environ.get("OPENAI_BASE_URL", None),
)
