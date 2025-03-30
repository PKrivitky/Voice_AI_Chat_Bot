from dataclasses import dataclass
import os
# from environs import Env
from dotenv import load_dotenv

load_dotenv()

@dataclass
class TgBot:
    token: str

@dataclass
class OpenAIConfig:
    api_key: str

@dataclass
class Config:
    tg_bot: TgBot
    openai: OpenAIConfig

def load_config() -> Config:
    return Config(tg_bot=TgBot(token=os.getenv('BOT_TOKEN')),
                  openai=OpenAIConfig(api_key=os.getenv('OPENAI_API_KEY')))
