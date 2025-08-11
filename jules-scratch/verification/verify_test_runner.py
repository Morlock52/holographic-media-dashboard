import asyncio
from playwright.async_api import async_playwright, expect

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        try:
            await page.goto("http://localhost:9999/test-runner.html", wait_until="load")

            # Click the button to run all tests
            await page.get_by_role("button", name="🚀 Run All Tests").click()

            # Wait for the test summary to appear
            await expect(page.get_by_text("Test Summary:")).to_be_visible(timeout=15000)

            # Check the status of the Navigation System test card
            nav_card = page.locator(".test-card", has_text="Navigation System")
            await expect(nav_card.get_by_text("PASS")).to_be_visible()

            # Check the status of the WebGL Rendering test card
            webgl_card = page.locator(".test-card", has_text="WebGL Rendering")
            await expect(webgl_card.get_by_text("FAIL")).to_be_visible()

            # Check for the final summary log
            await expect(page.locator("#testLog")).to_contain_text("Test Summary:")

            await page.screenshot(path="jules-scratch/verification/test_runner_fixed.png")
            print("Screenshot taken successfully.")

        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
