from contextlib import asynccontextmanager
from typing import AsyncGenerator

from playwright.async_api import BrowserContext, async_playwright

from app.config import PROFILE_DIR


@asynccontextmanager
async def browser_context(*, headless: bool = True) -> AsyncGenerator[BrowserContext, None]:
    """Async context manager that yields a persistent Chromium browser context."""
    PROFILE_DIR.mkdir(exist_ok=True)
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE_DIR),
            channel="chrome",
            headless=headless,
            args=["--disable-blink-features=AutomationControlled"],
        )
        try:
            yield context
        finally:
            await context.close()
