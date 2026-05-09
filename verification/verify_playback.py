import os
import time
from playwright.sync_api import sync_playwright, expect

def verify_playback():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        path = os.path.abspath("index.html")
        page.goto(f"file://{path}")

        # Click the first song
        first_song = page.locator("#song-list li").nth(0)
        first_song.click()

        initial_title = page.locator("#current-song-title").inner_text()
        print(f"Initial title: {initial_title}")

        # Manually trigger the 'ended' event on the audio element
        page.evaluate("audio.dispatchEvent(new Event('ended'))")

        # Check if it moved to the second song
        time.sleep(1) # Wait for UI update
        second_title = page.locator("#current-song-title").inner_text()
        print(f"Second title: {second_title}")

        if initial_title != second_title and second_title == "Breaded Soldier on the Line":
            print("SUCCESS: Continuous playback works!")
        else:
            print("FAILURE: Continuous playback failed.")
            exit(1)

        browser.close()

if __name__ == "__main__":
    verify_playback()
