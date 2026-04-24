import logging

from playwright.async_api import Page

from app.config import AUTH_CHECK_TIMEOUT_MS, XPATH_SIGN_IN_BTN

log = logging.getLogger(__name__)


async def is_logged_in(page: Page) -> bool:
    """Return True if an active Adobe session exists on the current page.

    Strategy: wait briefly for the "Sign In" button. If it appears the user is
    NOT logged in; if the wait times out the button is absent, meaning they ARE.
    """
    try:
        await page.locator(XPATH_SIGN_IN_BTN).wait_for(timeout=AUTH_CHECK_TIMEOUT_MS)
        log.warning("Adobe session not found — Sign In button is visible")
        return False
    except Exception:
        log.info("Adobe session active")
        return True
