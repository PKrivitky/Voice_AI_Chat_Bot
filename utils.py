import aiohttp
from config import load_config

config = load_config()

async def speech_to_text(file_url: str) -> str:
    url = "https://api.openai.com/v1/audio/transcriptions"
    headers = {"Authorization": f"Bearer {config.openai.api_key}"}
    
    async with aiohttp.ClientSession() as session:
        async with session.get(file_url) as resp:
            audio_data = await resp.read()

        form_data = aiohttp.FormData()
        form_data.add_field("file", audio_data, filename="audio.ogg")
        form_data.add_field("model", "whisper-1")

        async with session.post(url, headers=headers, data=form_data) as response:
            response_json = await response.json()
            return response_json.get("text", "Ошибка обработки")
        

async def get_openai_response(prompt: str) -> str:
    url = "https://api.openai.com/v1/completions"
    headers = {"Authorization": f"Bearer {config.openai.api_key}", "Content-Type": "application/json"}
    payload = {"model": "gpt-4-turbo", "messages": [{"role": "user", "content": prompt}]}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as response:
            response_json = await response.json()
            return response_json["choices"][0]["message"]["content"]


async def text_to_speech(text: str) -> bytes:
    url = "https://api.openai.com/v1/audio/speech"
    headers = {"Authorization": f"Bearer {config.openai.api_key}", "Content-Type": "application/json"}
    payload = {"model": "tts-1", "input": text, "voice": "alloy"}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as response:
            return await response.read()

