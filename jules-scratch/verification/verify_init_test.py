import asyncio
from playwright.async_api import async_playwright, expect

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        try:
            await page.goto("http://localhost:9999/init-test.html", wait_until="load")

            # Check that the expected failure message is present
            await expect(page.get_by_text("✗ THREE.js not loaded")).to_be_visible(timeout=5000)

            # Check that the CONFIG tests ran successfully
            await expect(page.get_by_text("✓ CONFIG loaded")).to_be_visible()

            print("Verification successful: Test page reports expected failure and successes.")
            await page.screenshot(path="jules-scratch/verification/init_test_fixed.png")

        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
