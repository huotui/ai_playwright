from typing import Dict, Optional
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
from app.config import settings
import threading
import time

class BrowserManager:
    _instance = None
    _browser: Optional[Browser] = None
    _contexts: Dict[str, BrowserContext] = {}
    _pages: Dict[str, Page] = {}
    _playwright = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = BrowserManager()
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self._playwright = sync_playwright().start()
        self._browser = self._playwright.chromium.launch(
            headless=settings.HEADLESS
        )

    def create_session(self, session_id: str) -> Page:
        context = self._browser.new_context(
            viewport={"width": settings.VIEWPORT_WIDTH, "height": settings.VIEWPORT_HEIGHT}
        )
        page = context.new_page()
        self._contexts[session_id] = context
        self._pages[session_id] = page
        return page

    def get_page(self, session_id: str) -> Optional[Page]:
        return self._pages.get(session_id)

    def close_session(self, session_id: str):
        if session_id in self._contexts:
            self._contexts[session_id].close()
            del self._contexts[session_id]
            del self._pages[session_id]

    def close_all(self):
        if self._browser:
            self._browser.close()
        if self._playwright:
            self._playwright.stop()
