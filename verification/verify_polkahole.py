import os
from playwright.sync_api import sync_playwright, expect

def verify_polkahole():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1280, 'height': 1600})
        page = context.new_page()

        # Load the local index.html
        path = os.path.abspath("index.html")
        page.goto(f"file://{path}")

        # Check for presence of key sections
        expect(page.locator("#welcome")).to_be_visible()
        expect(page.locator("#album")).to_be_visible()
        expect(page.locator("#music")).to_be_visible()
        expect(page.locator("#shows")).to_be_visible()
        expect(page.locator("#fan-zone")).to_be_visible()

        # Check for the accordion icon and title (using aria-label for animated text)
        expect(page.locator("h1")).to_have_attribute("aria-label", "POLKAHOLE")

        # Check the music player interactivity
        play_btn = page.locator("#play-pause-btn")
        expect(play_btn).to_have_text("Play")

        # Take a screenshot
        page.screenshot(path="verification/polkahole_final.png", full_page=True)

        browser.close()

if __name__ == "__main__":
    verify_polkahole()
