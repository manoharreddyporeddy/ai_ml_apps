import os
import openai
from openai import OpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

model_name = "gpt-4.1-mini"  # "gpt-4.1-mini", "gpt-4o-mini" works, You exceeded your current quota ("gpt-4.1", "gpt-3.5-turbo")
user_message = "Please tell me a joke."

print(f"\nModel: {model_name}")
print(f"Sending Message: {user_message}")

try:
    completion = client.chat.completions.create(
        model=model_name,
        store=True,
        messages=[{"role": "user", "content": user_message}],
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
