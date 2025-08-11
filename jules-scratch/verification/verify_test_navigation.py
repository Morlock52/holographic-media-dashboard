import asyncio
import re
from playwright.async_api import async_playwright, expect

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        console_messages = []
        page.on("console", lambda msg: console_messages.append(msg.text))

        error_message_to_show = ""

        try:
            await page.goto("http://localhost:9999/test-navigation.html", wait_until="load")

            # Check for the main title
            await expect(page.get_by_role("heading", name="Navigation Test Suite")).to_be_visible()

            # Check that the navigation-header component is rendered
            nav_header = page.locator("navigation-header")
            await expect(nav_header).to_be_visible()

            # Check the console logs for a valid page load time
            load_time_found = False
            for msg in console_messages:
                # Use a more robust regex that accounts for the emoji
                match = re.search(r"Page load time: (\d+)ms", msg)
                if match:
                    load_time = int(match.group(1))
                    if load_time > 0:
                        load_time_found = True
                        print(f"Found valid page load time: {load_time}ms")
                        break

            if not load_time_found:
                error_message_to_show = "Did not find a valid page load time in console logs."
                # Don't raise exception immediately, print logs first

            await page.screenshot(path="jules-scratch/verification/test_navigation_fixed.png")

            if error_message_to_show:
                raise Exception(error_message_to_show)

            print("Screenshot taken successfully.")

        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
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
