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

            # Check that the main title is visible (be specific to avoid strict mode violation)
            header_title = page.locator(".dashboard-header h1")
            await expect(header_title).to_be_visible()
            await expect(header_title).to_have_text("Service Dashboard")

            # Check that there is NO error message
            error_message = page.locator("#errorMessage")
            await expect(error_message).not_to_be_visible()

            # Check that the service grid is populated
            jellyfin_card = page.locator("#service-jellyfin")
            await expect(jellyfin_card).to_be_visible()
            await expect(jellyfin_card.get_by_text("Jellyfin")).to_be_visible()

            await page.screenshot(path="jules-scratch/verification/servicedash_fixed.png")
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
