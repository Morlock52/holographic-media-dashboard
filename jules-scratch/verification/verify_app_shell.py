import asyncio
import re
from playwright.async_api import async_playwright, expect

async def main():
    async with async_playwright() as p:
        # The test needs a mobile viewport to make the toggle button visible
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(**p.devices['iPhone 11'])
        page = await context.new_page()

        try:
            await page.goto("http://localhost:9999/app-shell.html", wait_until="load")

            # Check for the main title
            await expect(page.get_by_role("heading", name="Welcome to HoloMedia Hub")).to_be_visible()

            # Find the sidebar and the toggle button
            sidebar = page.locator("#sidebar")
            toggle_button = page.locator(".mobile-menu-toggle")

            # Initially, the sidebar should not have the 'open' class
            await expect(sidebar).not_to_have_class(re.compile(r'\bopen\b'))

            # Click the toggle button to open the menu
            await toggle_button.click()

            # Now the sidebar should have the 'open' class
            await expect(sidebar).to_have_class(re.compile(r'\bopen\b'))

            await page.screenshot(path="jules-scratch/verification/app_shell.png")
            print("Screenshot taken successfully.")

        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
