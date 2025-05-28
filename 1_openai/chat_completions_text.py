from openai import OpenAI
import os  # To access environment variables

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    store=True,
    messages=[{"role": "user", "content": "Please tell me a joke."}],
)

print(completion.choices[0].message.content)
