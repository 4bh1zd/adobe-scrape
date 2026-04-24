import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

async def run_scraper():
    async with Stealth().use_async(async_playwright()) as p:
        browser = await p.chromium.launch(headless=True)

        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("https://www.google.com/")

        title = await page.title()
        print("Page title:", title)

        await browser.close()