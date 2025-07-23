import asyncio
import json
from http.cookiejar import MozillaCookieJar
from playwright.async_api import async_playwright

# Cookies from facebook
COOKIES_FILE = "cookies.facebook.txt"

# URL to the saved items page
# SAVED_URL = "https://www.facebook.com/saved/?referrer=SAVE_DASHBOARD_NAVIGATION_PANEL"
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

#alternative URL
SAVED_URL = "https://www.facebook.com/saved/?dashboard_section=ALL"

# Function to convert Netscape format cookies to Playwright format
def convert_netscape_to_playwright(path):
    jar = MozillaCookieJar()
    jar.load(path, ignore_discard=True, ignore_expires=True)
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

# Function to unsave all visible items on the Facebook saved page
async def unsave_all_visible_items(max_rounds=20):
    cookies = convert_netscape_to_playwright(COOKIES_FILE)

    # Check if cookies are loaded
    async with async_playwright() as p:
        # Launch the browser with the loaded cookies ion this case: Chromium
        browser = await p.chromium.launch(headless=False)
        # browser = await p.firefox.launch(headless=False)
        # browser = await p.webkit.launch(headless=False)
        context = await browser.new_context(viewport={"width": 1200, "height": 800})
        await context.add_cookies(cookies)
        page = await context.new_page()

        # Navigate to the saved items page
        for round_num in range(max_rounds):
            print(f"\n🔁 Ronda #{round_num + 1}")
            # Increase the timeout to 60 seconds for the initial page load, modify as fits
            await page.goto(SAVED_URL, timeout=60000)
            await page.wait_for_timeout(2500)

            # Wait for the page to load
            try:
                all_more_buttons = await page.query_selector_all('div[aria-label="More"][role="button"]')
                if len(all_more_buttons) <= 1:
                    print("✅ No hay suficientes botones para procesar. Fin.")
                    break

                print(f"🔍 Botones 'More' encontrados: {len(all_more_buttons)} (ignorando el primero)")

                # Skip the first button as it is not needed
                processed = 0
                for idx, more_btn in enumerate(all_more_buttons[1:], start=1):
                    print(f"🔎 Botón #{idx}:")

                    try:
                        await more_btn.scroll_into_view_if_needed()
                        await more_btn.hover()
                        await page.wait_for_timeout(300)
                        await more_btn.click(timeout=2000)
                        await page.wait_for_timeout(1000)

                        unsave_spans = await page.query_selector_all("span.x193iq5w")
                        found = False
                        for span in unsave_spans:
                            try:
                                text = await span.inner_text()
                                if text.strip().lower() == "unsave":
                                    await span.click(timeout=3000)
                                    print(f"✅ Desguardado con botón #{idx}")
                                    found = True
                                    processed += 1
                                    break
                            except:
                                continue

                        if not found:
                            print(f"🚫 No se encontró 'Unsave' en botón #{idx}. Cerrando menú.")
                            await page.keyboard.press("Escape")
                            await page.wait_for_timeout(500)

                    except Exception as e:
                        print(f"⚠️ Falló botón #{idx}: {e}")

                print(f"📦 Ronda #{round_num + 1} completada. Ítems desguardados: {processed}")

                if processed == 0:
                    print("😴 No se desguardó nada en esta ronda. Posible fin.")
                    break

                await page.wait_for_timeout(2000)

            except Exception as e:
                print(f"❌ Error general en ronda #{round_num + 1}: {e}")
                break

        await browser.close()

# Run the unsave function modify the max_rounds as needed
asyncio.run(unsave_all_visible_items(max_rounds=50))