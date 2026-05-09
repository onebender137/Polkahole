import pytest
from playwright.sync_api import Page, expect

def test_album_display(page: Page):
    page.goto("http://localhost:8080/index.html")

    # Check for the main heading
    expect(page.locator("h2:has-text('Our Albums')")).to_be_visible()

    # Check for both album cards
    expect(page.locator("h4:has-text('Oompa Loompas and Syntax Errors')")).to_be_visible()
    expect(page.locator("h4:has-text(\"Polkin' the Hole\")")).to_be_visible()

    # Check for both album covers
    expect(page.locator("img[alt='Oompa Loompas and Syntax Errors CD Cover Art']")).to_be_visible()
    expect(page.locator("img[alt=\"Polkin' the Hole CD Cover Art\"]")).to_be_visible()

def test_track_counts(page: Page):
    page.goto("http://localhost:8080/index.html")

    # Oompa Loompas should have 12 tracks
    oompa_tracks = page.locator(".album-card").filter(has_text="Oompa Loompas and Syntax Errors").locator(".tracklist li")
    expect(oompa_tracks).to_have_count(12)

    # Polkin' the Hole should have 13 tracks
    polkin_tracks = page.locator(".album-card").filter(has_text="Polkin' the Hole").locator(".tracklist li")
    expect(polkin_tracks).to_have_count(13)

def test_player_art_switching(page: Page):
    page.goto("http://localhost:8080/index.html")

    player_art = page.locator("#player-album-art")

    # Load first song (Oompa Loompas)
    page.locator("#song-list li").nth(0).click()
    expect(player_art).to_have_attribute("src", "Gemini_Generated_Image_tevx5btevx5btevx.png")

    # Load 13th song (Polkin' the Hole)
    page.locator("#song-list li").nth(12).click()
    expect(player_art).to_have_attribute("src", "Gemini_Generated_Image_6sl51i6sl51i6sl5.png")
