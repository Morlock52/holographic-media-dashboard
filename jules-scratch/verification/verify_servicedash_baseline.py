import asyncio
from playwright.async_api import async_playwright, expect

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        console_messages = []
        page.on("console", lambda msg: console_messages.append(f"[{msg.type}] {msg.text}"))

        try:
            await page.goto("http://localhost:9999/service-dashboard.html", wait_until="networkidle")

            # Check for the main title
            await expect(page.get_by_text("Service Dashboard", exact=True)).to_be_visible()

            # Check for the error message
            error_message = page.locator("#errorMessage")
            await expect(error_message).to_be_visible()
            await expect(error_message).to_contain_text("Failed to initialize service monitoring")

            # The grid should be empty
            grid = page.locator("#servicesGrid")
            await expect(grid).to_contain_text("No services found")

            await page.screenshot(path="jules-scratch/verification/servicedash_baseline.png")
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
