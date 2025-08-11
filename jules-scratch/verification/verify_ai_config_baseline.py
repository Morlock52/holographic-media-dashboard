import asyncio
from playwright.async_api import async_playwright, expect

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        console_messages = []
        page.on("console", lambda msg: console_messages.append(f"[{msg.type}] {msg.text}"))

        try:
            await page.goto("http://localhost:9999/ai-config-manager.html", wait_until="load")

            # Check that the page title is visible
            await expect(page.get_by_role("heading", name="AI Config Manager")).to_be_visible()

            # Check that the AI Assistant panel is rendered
            await expect(page.get_by_text("AI Assistant", exact=True)).to_be_visible()

            # This page should load, but with console errors from the CDN
            print("Page loaded. Checking console for expected errors...")

        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            # Check for expected errors
            cdn_errors = [msg for msg in console_messages if "cdnjs.cloudflare.com" in msg]
            if cdn_errors:
                print(f"✓ Found {len(cdn_errors)} expected CDN loading errors.")
            else:
                print("✗ Did not find expected CDN loading errors.")

            print("\n--- Console Messages ---")
            if console_messages:
                for msg in console_messages:
                    print(msg)
            else:
                print("No console messages were captured.")
            print("------------------------\n")

            await page.screenshot(path="jules-scratch/verification/ai_config_baseline.png")
            print("Screenshot taken.")
            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
