import asyncio
from playwright.async_api import async_playwright, expect

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        console_messages = []
        page.on("console", lambda msg: console_messages.append(f"[{msg.type}] {msg.text}"))

        try:
            await page.goto("http://localhost:9999/config-manager.html", wait_until="networkidle")

            # Check for the main title
            await expect(page.get_by_text("Configuration Manager")).to_be_visible()

            # Find and expand the "Authentication" group
            auth_header = page.locator(".env-group[data-group='auth'] .env-group-header")
            await auth_header.click()

            # Check if the body is now visible
            auth_body = page.locator(".env-group[data-group='auth'] .env-group-body")
            await expect(auth_body).to_be_visible()

            # Check the value of the default user input
            user_input = page.locator("input[data-key='AUTHELIA_DEFAULT_USER']")
            await expect(user_input).to_have_value("admin")

            await page.screenshot(path="jules-scratch/verification/config_manager_baseline.png")
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
