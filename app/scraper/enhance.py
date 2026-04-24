import asyncio
import logging
import random
from pathlib import Path

from app.config import (
    ADOBE_URL,
    PAUSE_MAX_S,
    PAUSE_MIN_S,
    PROCESSING_TIMEOUT_MS,
    XPATH_DOWNLOAD_BTN,
    XPATH_UPLOAD_BTN,
    XPATH_VERSION_ITEM,
    XPATH_VERSION_PICKER,
)
from app.scraper.auth import is_logged_in
from app.scraper.browser import browser_context

log = logging.getLogger(__name__)


async def _pause(min_s: float = PAUSE_MIN_S, max_s: float = PAUSE_MAX_S) -> None:
    await asyncio.sleep(random.uniform(min_s, max_s))


async def enhance_audio(input_path: Path, output_dir: Path = Path(".")) -> Path:
    """Upload *input_path* to Adobe Podcast Enhance and save the result to *output_dir*.

    Requires an active Adobe session — run `python -m app login` first.

    Returns the path of the downloaded output file.
    """
    input_path = Path(input_path).resolve()
    output_dir = Path(output_dir)

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    output_dir.mkdir(parents=True, exist_ok=True)
    log.info("Starting Adobe Enhance — input: %s", input_path.name)

    async with browser_context(headless=True) as context:
        log.info("Browser launched")
        page = await context.new_page()

        log.info("Navigating to Adobe Enhance")
        await page.goto(ADOBE_URL)
        await _pause(2.0, 4.0)

        if not await is_logged_in(page):
            raise RuntimeError("Not logged in. Run `python -m app login` first.")

        log.info("Selecting enhancement version")
        await page.locator(XPATH_VERSION_PICKER).locator("button").click()
        await _pause()
        await page.locator(XPATH_VERSION_ITEM).click()
        await _pause()

        log.info("Uploading %s", input_path.name)
        async with page.expect_file_chooser() as fc:
            await page.locator(XPATH_UPLOAD_BTN).click()
        await _pause(0.5, 1.5)
        await (await fc.value).set_files(str(input_path))
        log.info("File uploaded — waiting for processing (up to 5 min)")

        download_btn = page.locator(XPATH_DOWNLOAD_BTN)
        await download_btn.wait_for(timeout=PROCESSING_TIMEOUT_MS)
        log.info("Processing complete — initiating download")
        await _pause()

        async with page.expect_download() as dl:
            await download_btn.click()
        download = await dl.value
        out_path = output_dir / f"output-{download.suggested_filename}"
        await download.save_as(str(out_path))
        log.info("Saved to %s", out_path)

    log.info("Done")
    return out_path
