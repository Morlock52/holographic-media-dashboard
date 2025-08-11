import asyncio
from playwright.async_api import async_playwright, expect

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        try:
            await page.goto("http://localhost:9999/test-simple.html", wait_until="load")

            # The page just shows a loading screen and then hides it.
            # We'll wait for the loading screen to become hidden.
            loading_screen = page.locator("#loading-screen")
            await expect(loading_screen).to_be_hidden(timeout=5000)

            print("Verification successful: loading screen was hidden.")

        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
