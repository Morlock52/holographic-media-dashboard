import asyncio
from playwright.async_api import async_playwright, expect

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Array to store console messages
        console_messages = []

        # Listen for console events and store them
        page.on("console", lambda msg: console_messages.append(f"[{msg.type}] {msg.text}"))

        try:
            # Navigate to the page
            await page.goto("http://localhost:9999/index.html", wait_until="networkidle")

            # Wait for the loading screen to disappear, with a generous timeout
            loading_screen = page.locator("#loading-screen")
            await expect(loading_screen).to_be_hidden(timeout=15000)

            # A small extra wait to ensure scripts after loading have run
            await page.wait_for_timeout(2000)

            # Take a screenshot
            await page.screenshot(path="jules-scratch/verification/baseline_index.png")
            print("Screenshot taken successfully.")

        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            # Print all captured console messages
            print("\n--- Console Messages ---")
            if console_messages:
                for msg in console_messages:
                    print(msg)
            else:
                print("No console messages were captured.")
            print("------------------------\n")

            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
