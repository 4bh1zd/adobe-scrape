import asyncio
import logging

from app.config import ADOBE_URL, LOGIN_POLL_INTERVAL_S, PROFILE_DIR
from app.scraper.auth import is_logged_in
from app.scraper.browser import browser_context

log = logging.getLogger(__name__)


async def login() -> None:
    """Open a visible browser so the user can authenticate with Adobe manually.

    Polls until login is detected, then saves the session to PROFILE_DIR.
    """
    async with browser_context(headless=False) as context:
        page = await context.new_page()
        await page.goto(ADOBE_URL)

        if await is_logged_in(page):
            log.info("Already logged in — nothing to do")
            return

        log.info("Please log in manually in the browser window")
        while not await is_logged_in(page):
            await asyncio.sleep(LOGIN_POLL_INTERVAL_S)

        log.info("Login detected — session saved to %s", PROFILE_DIR)
