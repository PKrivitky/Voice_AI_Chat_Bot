from test_config import OPENAI_API_KEY
from test_config import BOT_TOKEN
import asyncio
import time
from aiogram.types import Message, Voice
from aiogram import Router, Bot, Dispatcher
from openai import OpenAI
from aiogram.client.bot import DefaultBotProperties
from aiogram.types import FSInputFile

client = OpenAI(api_key=OPENAI_API_KEY)
router = Router()
bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))

@router.message()
async def handle_voice_massage(message: Message):
    chat_id = str(message.chat.id)
    unique_name = str(int(time.time()))
    save_path = f'{unique_name}.ogg'
    file_id = message.voice.file_id
    file = await bot.get_file(file_id=str(file_id))
    await bot.download_file(file.file_path, save_path)
    try:
        speech_text = await stt(f'{save_path}')
    except Exception as e:
        await message.reply(str(e))
        return
    
    gpt_answer = await ask_gpt(speech_text)

    unique_name = str(int(time.time()))
    save_path = f'{unique_name}.ogg'
    await tts(gpt_answer, save_path)
    audio_file = FSInputFile(f'{save_path}')
    await bot.send_voice(voice=audio_file, chat_id=chat_id)

async def stt(unique_name):
    audio_file = open(f'{unique_name}', 'rb')
    transcription = client.audio.transcriptions.create(
        model='whisper-1',
        file=audio_file
    )
    print(transcription.text)
    return(transcription.text)

async def tts(text, unique_name):
    speech_file_path = f'{unique_name}'
    response = client.audio.speech.create(
        model='tts-1',
        voice='alloy',
        input=f'{text}'
    )
    with open(speech_file_path, 'wb') as f:
        f.write(response.content)
    print('finish')

async def ask_gpt(text):
    response = client.chat.completions.create(
        model='gpt-4o',
        messages=[{"role": "system", "content": "f{text}"},]
    )
    return response.choices[0].message.content

async def main():
    print("Start....")
    bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
    dp = Dispatcher()

    dp.include_routers(router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())