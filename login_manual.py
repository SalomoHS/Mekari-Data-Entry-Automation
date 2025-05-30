import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        # Launch a visible (headed) browser
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()

        page = await context.new_page()

        # Go to the login page
        await page.goto("https://github.com/login")

        print("🔒 Please log in manually. The script will wait until you're logged in...")

        # Wait for some element that only appears after login
        # e.g., a dashboard button, user profile icon, etc.
        await page.wait_for_selector("#dashboard", timeout=0)

        print("✅ Logged in! Continuing automation...")

        # Now continue automation after login
        await page.click("#dashboard")

        # More automation here...
        await asyncio.sleep(5)

        await browser.close()

asyncio.run(main())
