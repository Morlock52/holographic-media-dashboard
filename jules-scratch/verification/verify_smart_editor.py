import asyncio
from playwright.async_api import async_playwright, expect

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        try:
            await page.goto("http://localhost:9999/smart-env-editor.html", wait_until="load")

            # Check for the main title
            await expect(page.locator("navigation-header")).to_be_visible()

            # Wait for the editor to be populated
            editor = page.locator("#envEditor")
            await expect(editor).to_contain_text("NODE_ENV=development", timeout=5000)

            # Check that line numbers were rendered
            line_numbers = page.locator("#lineNumbers")
            # The sample env has 26 lines
            await expect(line_numbers).to_contain_text("26")

            print("Verification successful: Editor and line numbers are populated.")
            await page.screenshot(path="jules-scratch/verification/smart_env_editor_restored.png")

        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
