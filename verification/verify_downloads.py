import asyncio
from playwright.async_api import async_playwright
import os

async def verify_downloads():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Get absolute path to index.html
        file_path = f"file://{os.path.abspath('index.html')}"
        await page.goto(file_path)

        # Verify Album Download Links
        album_zips = ["Oompa_Loompas_and_Syntax_Errors.zip", "Polkin_the_Hole.zip"]
        for zip_name in album_zips:
            link = page.locator(f"a[href='{zip_name}']")
            await link.wait_for(state="visible")
            print(f"Found album download link: {zip_name}")

        # Verify Music Player Download Link
        download_link = page.locator("#download-song-link")
        # Initially hidden
        is_hidden = await download_link.is_hidden()
        print(f"Download song link is initially hidden: {is_hidden}")

        # Select a song
        first_song = page.locator("#song-list li").first
        await first_song.click()

        # Should be visible now
        await download_link.wait_for(state="visible")
        href = await download_link.get_attribute("href")
        download_attr = await download_link.get_attribute("download")
        print(f"Download song link visible. href: {href}, download: {download_attr}")

        # Take screenshot
        await page.screenshot(path="verification/downloads_verify.png", full_page=True)
        print("Screenshot saved to verification/downloads_verify.png")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(verify_downloads())
