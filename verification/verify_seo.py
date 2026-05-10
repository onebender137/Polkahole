import asyncio
import os
from playwright.async_api import async_playwright

async def verify_seo_metadata():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        path = os.path.abspath('index.html')
        page = await browser.new_page()

        # Load a specific song via query parameter
        await page.goto(f'file://{path}?song=0')
        await page.wait_for_selector('#current-song-title')

        # 1. Verify document title
        title = await page.title()
        assert "Boots on the Floorboards" in title, f"Title should contain song name, got: {title}"

        # 2. Verify meta description
        description = await page.get_attribute('meta[name="description"]', 'content')
        assert "Boots on the Floorboards" in description, f"Description should contain song name, got: {description}"

        # 3. Verify Open Graph tags
        og_title = await page.get_attribute('meta[property="og:title"]', 'content')
        assert "Boots on the Floorboards" in og_title, f"OG Title should contain song name, got: {og_title}"

        og_url = await page.get_attribute('meta[property="og:url"]', 'content')
        assert "song=0" in og_url, f"OG URL should contain song=0, got: {og_url}"

        # 4. Verify Twitter tags
        twitter_image = await page.get_attribute('meta[property="twitter:image"]', 'content')
        assert "Gemini_Generated_Image_tevx5btevx5btevx.png" in twitter_image, f"Twitter image should be album art, got: {twitter_image}"

        # 5. Verify Canonical link
        canonical = await page.get_attribute('link[rel="canonical"]', 'href')
        assert "song=0" in canonical, f"Canonical link should contain song=0, got: {canonical}"

        print("SUCCESS: SEO Metadata updates verified!")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(verify_seo_metadata())
