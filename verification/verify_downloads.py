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
        # Album 0
        await page.locator(".album-thumb[data-album='0']").click()
        link0 = page.locator("a[href='Oompa_Loompas_and_Syntax_Errors.zip']")
        await link0.wait_for(state="visible")
        print("Found album download link: Oompa_Loompas_and_Syntax_Errors.zip")

        # Album 1
        await page.locator(".album-thumb[data-album='1']").click()
        link1 = page.locator("a[href='Polkin_the_Hole.zip']")
        await link1.wait_for(state="visible")
        print("Found album download link: Polkin_the_Hole.zip")

        # Album 2 (Whoa Polka!)
        await page.locator(".album-thumb[data-album='2']").click()
        link2 = page.locator("a[href='Whoa_Polka.zip']")
        await link2.wait_for(state="visible")
        print("Found album download link: Whoa_Polka.zip")

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
        await page.screenshot(path="verification/downloads_verify.webp", full_page=True)
        print("Screenshot saved to verification/downloads_verify.webp")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(verify_downloads())
