import asyncio
from playwright.async_api import async_playwright, expect

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        try:
            # --- Test 1: Automatic Redirection ---
            print("Testing automatic redirection...")
            await page.goto("http://localhost:9999/splash-screen.html", wait_until="load")

            # Take a screenshot mid-animation
            await page.wait_for_timeout(2000)
            await page.screenshot(path="jules-scratch/verification/splash_screen.png")
            print("Screenshot of splash screen taken.")

            # Wait for the redirection to complete
            await page.wait_for_url("**/main-app.html", timeout=10000)
            print("Automatic redirection to main-app.html successful.")


            # --- Test 2: Skip Intro Button ---
            print("\nTesting 'Skip Intro' button...")
            await page.goto("http://localhost:9999/splash-screen.html", wait_until="load")

            # Click the skip button
            skip_button = page.get_by_role("button", name="Skip Intro")
            await expect(skip_button).to_be_visible()
            await skip_button.click()

            # Wait for the redirection to complete
            await page.wait_for_url("**/main-app.html", timeout=5000)
            print("'Skip Intro' button redirection successful.")

            print("\nSplash screen verification successful.")

        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
