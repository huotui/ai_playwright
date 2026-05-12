import os
from pathlib import Path
from dotenv import load_dotenv

# 加载项目根目录的 .env 文件
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

class Settings:
    APP_NAME: str = "AI Playwright MCP"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "key")
    OPENAI_API_BASE: str = os.getenv("OPENAI_API_BASE", "http://172.22.176.1:1234/v1")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "google/gemma-4-26b-a4b")
    
    DATABASE_URL: str = "sqlite:///./ai_playwright.db"
    
    BROWSER_TYPE: str = "chromium"
    HEADLESS: bool = True
    VIEWPORT_WIDTH: int = 1280
    VIEWPORT_HEIGHT: int = 720
    
    MAX_RETRIES: int = 3
    TIMEOUT_MS: int = 30000
    
    BROWSER_POOL_SIZE: int = 3

settings = Settings()
