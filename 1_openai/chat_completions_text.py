import os
import openai
from openai import OpenAI

MODEL_NAME = "gpt-4.1-mini"  # gpt-4.1-mini/gpt-4o-mini works, gpt-4.1/gpt-3.5-turbo does not work
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)
print(f"\nModel: {MODEL_NAME}")

try:
    USER_MESSAGE = "Please tell me a joke."
    print(f"Sending Message: {USER_MESSAGE}")

    completion = client.chat.completions.create(
        model=MODEL_NAME,
        store=True,
        messages=[{"role": "user", "content": USER_MESSAGE}],
    )
    print(f"Response: {completion.choices[0].message.content}")

except openai.RateLimitError as e:
    # Handle rate limit error (we recommend using exponential backoff)
    print(f"OpenAI API request exceeded rate limit: {e}")
except openai.APIConnectionError as e:
    # Handle connection error here
    print(f"Failed to connect to OpenAI API: {e}")
except openai.APIError as e:
    # Handle API error here, e.g. retry or log
    print(f"OpenAI API returned an API Error: {e}")
