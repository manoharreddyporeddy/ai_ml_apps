# real-time weather data

import os
import json
import requests
from openai import OpenAI

MODEL_NAME = "gpt-4.1-mini"  # gpt-4.1-mini/gpt-4o-mini works, gpt-4.1/gpt-3.5-turbo does not work
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)
print(f"\nModel: {MODEL_NAME}")


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
    model=MODEL_NAME,
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
            model=MODEL_NAME,
            messages=messages,
            tools=tools,
        )
        print(completion_2.choices[0].message.content)


else:
    print("\n🤖 GPT didn't call a tool.")
    print(completion.choices[0].message.content)

# =========== FORCE TOOL ========

# real-time weather data

import os
import json
import requests
from openai import OpenAI

MODEL_NAME = "gpt-4.1-mini"  # gpt-4.1-mini/gpt-4o-mini works
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)
print(f"\nModel: {MODEL_NAME}")

# Dummy geocoder for demo purposes
def my_get_city_coordinates(city):
    # In production, use an API like OpenCage or Google Maps
    city = city.lower()
    coordinates = {
        "paris": {"latitude": 48.8566, "longitude": 2.3522},
        "new york": {"latitude": 40.7128, "longitude": -74.0060},
        "tokyo": {"latitude": 35.6762, "longitude": 139.6503},
    }
    return coordinates.get(city, {"latitude": 0, "longitude": 0})


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
            "name": "get_city_coordinates",
            "description": "Get latitude and longitude for a city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string"},
                },
                "required": ["city"],
            },
        },
    },
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
        },
    }
]

messages = [
    {
        "role": "system",
        "content": "Always use the tools to respond. First get coordinates from city name if needed, then fetch weather.",
    },
    {
        "role": "user",
        "content": "What's the weather like in Paris today?",
    }
]

# Step 1: Let GPT decide which tool to call first
completion = client.chat.completions.create(
    model=MODEL_NAME,
    messages=messages,
    tools=tools,
    tool_choice="auto",
)

if completion.choices[0].message.tool_calls:
    tool_call = completion.choices[0].message.tool_calls[0]
    function_name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)

    if function_name == "get_city_coordinates":
        coords = my_get_city_coordinates(**args)
        print(f"City coordinates: {coords}")

        messages.append(completion.choices[0].message)
        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(coords),
            }
        )

        # Step 2: Ask GPT again with updated context, now it should call get_weather
        completion_2 = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            tools=tools,
        )

        if completion_2.choices[0].message.tool_calls:
            tool_call_2 = completion_2.choices[0].message.tool_calls[0]
            function_name = tool_call_2.function.name
            args = json.loads(tool_call_2.function.arguments)

            if function_name == "get_weather":
                result = my_get_weather(**args)
                print(f"Temperature: {result}")

                messages.append(completion_2.choices[0].message)
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call_2.id,
                        "content": str(result),
                    }
                )

                final_completion = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=messages,
                    tools=tools,
                )
                print(final_completion.choices[0].message.content)
        else:
            print("🤖 Second tool call not made.")
    elif function_name == "get_weather":
        # Fallback case: model jumped directly to weather
        result = my_get_weather(**args)
        print(f"Temperature: {result}")
else:
    print("🤖 GPT didn't call any tool.")
    print(completion.choices[0].message.content)

# ============
