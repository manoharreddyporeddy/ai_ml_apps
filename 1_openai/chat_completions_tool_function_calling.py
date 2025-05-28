# real-time weather data

import os
import requests
from openai import OpenAI
import json


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)
model_name = "gpt-4.1-mini"  # "gpt-4.1-mini"/"gpt-4o-mini" works, "gpt-4.1", "gpt-3.5-turbo" does not work (You exceeded your current quota)
user_message = "Please tell me a joke."


def my_get_weather(latitude, longitude):
    response = requests.get(
        f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m",
        timeout=10,
    )
    data = response.json()
    return data["current"]["temperature_2m"]


tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current temperature for provided coordinates in celsius.",
            "parameters": {
                "type": "object",
                "properties": {
                    "latitude": {"type": "number"},
                    "longitude": {"type": "number"},
                },
                "required": ["latitude", "longitude"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    }
]
messages = [
    {
        "role": "user",
        "content": "What's the weather like in Paris today?",
    }
]
completion = client.chat.completions.create(
    model=model_name,
    messages=messages,
    tools=tools,
)


if completion.choices[0].message.tool_calls:
    tool_call = completion.choices[0].message.tool_calls[0]
    function_name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)

    if function_name == "get_weather":
        result = my_get_weather(**args)
        print(result)

        messages.append(completion.choices[0].message)
        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result),
            }
        )
        completion_2 = client.chat.completions.create(
            model=model_name,
            messages=messages,
            tools=tools,
        )
        print(completion_2.choices[0].message.content)


else:
    print("\n🤖 GPT didn't call a tool.")
    print(completion.choices[0].message.content)
