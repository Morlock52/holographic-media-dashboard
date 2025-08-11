import asyncio
from playwright.async_api import async_playwright, expect

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        try:
            await page.goto("http://localhost:9999/test.html", wait_until="load")

            # Wait for all the script loading tests to finish
            await expect(page.get_by_text("All scripts loaded!")).to_be_visible(timeout=10000)

            # Check for the expected FAILURE of THREE.js loading
            await expect(page.get_by_text("✗ THREE.js failed to load")).to_be_visible()

            # Check for the successful definition of the main class
            await expect(page.get_by_text("✓ HolographicMediaDashboard class is defined")).to_be_visible()

            # Check for the successful definition of the scene class
            await expect(page.get_by_text("✓ HolographicScene class is defined")).to_be_visible()

            await page.screenshot(path="jules-scratch/verification/test_page_fixed.png")
            print("Screenshot taken successfully.")

        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
