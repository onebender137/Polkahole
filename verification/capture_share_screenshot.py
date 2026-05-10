import asyncio
import os
from playwright.async_api import async_playwright

async def capture_share_modal():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        path = os.path.abspath('index.html')
        page = await browser.new_page()
        await page.goto(f'file://{path}')

        # Load a song
        await page.locator('.album-card.active .tracklist li').first.click()
        await page.wait_for_selector('#share-song-btn', state='visible')

        # Click share button
        await page.locator('#share-song-btn').click()

        # Wait for modal
        await page.wait_for_selector('#share-modal', state='visible')

        # Take screenshot of the modal
        await page.screenshot(path='verification/share_modal_screenshot.png')

        print("Screenshot captured at verification/share_modal_screenshot.png")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(capture_share_modal())
