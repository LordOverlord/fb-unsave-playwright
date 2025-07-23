import asyncio
import json
import os
from http.cookiejar import MozillaCookieJar
from playwright.async_api import async_playwright
from datetime import datetime


timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
NETSCAPE_COOKIES_FILE = "cookies.facebook.txt"   # cookies en formato Netscape
OUTPUT_FILE = f"facebook_saved_links_{timestamp}.txt"
# URL to the saved items page
FACEBOOK_SAVED_URL = "https://www.facebook.com/saved/?referrer=SAVE_DASHBOARD_NAVIGATION_PANEL"
# Alternate URLS
# SAVED_URL = "https://www.facebook.com/saved/?cref=28"
# SAVED_URL = "https://www.facebook.com/saved/?dashboard_section=LINKS"
# SAVED_URL = "https://www.facebook.com/saved/?dashboard_section=VIDEOS"
# SAVED_URL = "https://www.facebook.com/saved/?dashboard_section=REELS"
# SAVED_URL = "https://www.facebook.com/saved/?dashboard_section=PHOTOS"
# SAVED_URL = "https://www.facebook.com/saved/?dashboard_section=PLACES"
# SAVED_URL = "https://www.facebook.com/saved/?dashboard_section=PRODUCTS"
# SAVED_URL = "https://www.facebook.com/saved/?dashboard_section=EVENTS"
# SAVED_URL = "https://www.facebook.com/saved/?dashboard_section=OFFERS"
# SAVED_URL = "https://www.facebook.com/saved/?dashboard_section=UNLISTED"
# SAVED_URL = "https://www.facebook.com/saved/?dashboard_section=ALL"

def convert_netscape_to_playwright(netscape_file):
    jar = MozillaCookieJar()
    jar.load(netscape_file, ignore_discard=True, ignore_expires=True)

    cookies = []
    for c in jar:
        cookies.append({
            "name": c.name,
            "value": c.value,
            "domain": c.domain,
            "path": c.path,
            "expires": c.expires,
            "httpOnly": False,
            "secure": c.secure,
            "sameSite": "Lax"
        })
    return cookies

async def run():
    cookies = convert_netscape_to_playwright(NETSCAPE_COOKIES_FILE)

    async with async_playwright() as p:
        # Launch the browser with the loaded cookies in this case: Chromium
        browser = await p.chromium.launch(headless=False)
        # browser = await p.firefox.launch(headless=False)
        # browser = await p.webkit.launch(headless=False)
        context = await browser.new_context()
        await context.add_cookies(cookies)

        page = await context.new_page()
        await page.goto(FACEBOOK_SAVED_URL)

        # Scroll infinito
        previous_height = 0
        while True:
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(2000)
            new_height = await page.evaluate("document.body.scrollHeight")
            if new_height == previous_height:
                break
            previous_height = new_height

        # Extraer y guardar enlaces únicos
        links = await page.eval_on_selector_all("a[href]", "els => els.map(el => el.href)")
        saved_links = sorted(set(link for link in links if "facebook.com" in link and "/saved" not in link))

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            for link in saved_links:
                f.write(link + "\n")

        print(f"✅ Enlaces guardados en {os.path.abspath(OUTPUT_FILE)} ({len(saved_links)} total)")
        await browser.close()

asyncio.run(run())
