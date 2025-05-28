# text_to_speech_with_voice_cloning_xtts_coqui.py
"""
Text-to-speech synthesis using Coqui XTTS with reference voice cloning support.
"""

import os  # To access environment variables (like your Hugging Face token)
from gradio_client import (
    Client,
)  # Gradio's client for calling models hosted on Hugging Face Spaces
import shutil  # To copy the output file from a temp folder to your local directory

# Step 1: Initialize the client to connect to Coqui XTTS model
# 'coqui/xtts' is the model name, and we pass your Hugging Face token (stored securely in environment)
client = Client("coqui/xtts", hf_token=os.getenv("HF_TOKEN"))

# Step 2: Send a request to the model to synthesize speech
result = client.predict(
    "Hello yay!",  # The text you want converted to speech
    "en",  # Language code ('en' for English)
    "https://cdn-uploads.huggingface.co/production/uploads/63d52e0c4e5642795617f668/V6-rMmI-P59DA4leWDIcK.wav",
    # Reference voice sample: helps the model mimic this person's voice
    None,  # Mic input (we're not using a mic recording here)
    False,  # Don't use microphone
    False,  # Don't cleanup reference voice after use
    False,  # Don’t automatically detect language (we already specified it)
    True,  # Agree to model's Terms of Service
    fn_index=1,  # This tells Gradio which function on the web app to call — each model may expose multiple
)

# Step 3: Get the synthesized audio file path from the result tuple
generated_audio_path = result[
    1
]  # result[1] is the output .wav file path (in temp folder)

# Step 4: Copy that file to your working folder as 'output.wav'
shutil.copyfile(generated_audio_path, "output.wav")

# Step 5: Let the user know it's done
print("TTS output saved to output.wav")
