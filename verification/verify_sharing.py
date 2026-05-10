import asyncio
import os
from playwright.async_api import async_playwright
import urllib.parse

async def verify_sharing():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        # Use absolute path for index.html
        path = os.path.abspath('index.html')
        page = await browser.new_page()
        await page.goto(f'file://{path}')

        # 1. Verify Share button is hidden initially
        share_btn = page.locator('#share-song-btn')
        assert await share_btn.is_hidden(), "Share button should be hidden initially"

        # 2. Load a song and verify Share button appears
        # Click the first track in the first album card
        await page.locator('.album-card.active .tracklist li').first.click()
        await page.wait_for_selector('#share-song-btn', state='visible')
        assert await share_btn.is_visible(), "Share button should be visible after loading a song"

        # 3. Click Share and verify modal appears
        await share_btn.click()
        modal = page.locator('#share-modal')
        await page.wait_for_selector('#share-modal', state='visible')
        assert await modal.is_visible(), "Share modal should be visible after clicking Share"

        # 4. Verify social links have correct URLs
        # Note: Index 0 is "Boots on the Floorboards"
        x_link = page.locator('#share-x')
        href = await x_link.get_attribute('href')
        decoded_href = urllib.parse.unquote(href)
        assert 'song=0' in decoded_href, f"X share link should contain song=0, got {decoded_href}"

        fb_link = page.locator('#share-fb')
        href = await fb_link.get_attribute('href')
        decoded_href = urllib.parse.unquote(href)
        assert 'song=0' in decoded_href, f"FB share link should contain song=0, got {decoded_href}"

        # 5. Verify Copy Link button exists
        copy_btn = page.locator('#share-copy')
        assert await copy_btn.is_visible(), "Copy link button should be visible"

        # 6. Verify Close Modal
        await page.locator('.close-modal').click()
        await page.wait_for_selector('#share-modal', state='hidden')
        assert await modal.is_hidden(), "Share modal should be hidden after clicking close"

        # 7. Verify loading via query param
        await page.goto(f'file://{path}?song=5')
        # Wait for the player to update
        await page.wait_for_selector('#current-song-title')
        title = await page.inner_text('#current-song-title')
        # Song index 5 is "Lose Your Shoes"
        assert title == "Lose Your Shoes", f"Expected song 'Lose Your Shoes', but got '{title}'"
        assert await share_btn.is_visible(), "Share button should be visible when loaded via query param"

        print("SUCCESS: Sharing functionality verified!")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(verify_sharing())
