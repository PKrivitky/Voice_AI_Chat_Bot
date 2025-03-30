import aiohttp
import os
from aiogram import Router
from aiogram.types import Message, Voice
from aiogram.filters import CommandStart
from config import Config, load_config
from utils import speech_to_text, get_openai_response, text_to_speech

router = Router()
config = load_config()

# Приветственное сообщение
@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("Привет! Отправь голосовое сообщение.")

# Обработка голосовых сообщений
@router.message(Voice)
async def handle_voice(message: Message, bot):
    voice = message.voice
    file_info = await bot.get_file(voice.file_id)
    file_path = file_info.file_path
    file_url = f"https://api.telegram.org/file/bot{config.tg_bot.token}/{file_path}"

    # 1. Распознавание голоса (Whisper)
    text = await speech_to_text(file_url)
    await message.answer(f"Ты сказал: {text}")

    # 2. Ответ от GPT-4
    response_text = await get_openai_response(text)
    await message.answer(f"Бот: {response_text}")

    # 3. Преобразование ответа в голос (TTS)
    audio_data = await text_to_speech(response_text)

    # 4. Отправка голосового ответа
    with open("response.ogg", "wb") as f:
        f.write(audio_data)
    
    with open("response.ogg", "rb") as audio:
        await message.answer_voice(audio)
    
    os.remove("response.ogg")
