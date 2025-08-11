import asyncio
import re
from playwright.async_api import async_playwright, expect

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={ 'width': 1280, 'height': 800 })
        page = await context.new_page()

        try:
            # 1. Screenshot splash-screen.html
            print("Capturing screenshot for splash-screen.html...")
            await page.goto("http://localhost:9999/splash-screen.html", wait_until="load")
            await page.wait_for_timeout(2000) # Wait for animation to be visible
            await page.screenshot(path="docs/screenshots/01_splash_screen.png")
            print("✓ Screenshot saved to docs/screenshots/01_splash_screen.png")

            # 2. Screenshot main-app.html shell
            print("\nCapturing screenshot for main-app.html shell...")
            await page.goto("http://localhost:9999/main-app.html", wait_until="load")
            await expect(page.locator(".sidebar")).to_be_visible()
            await page.screenshot(path="docs/screenshots/02_main_app_shell.png")
            print("✓ Screenshot saved to docs/screenshots/02_main_app_shell.png")

            # 3. Screenshot service-dashboard.html integration
            print("\nCapturing screenshot for service-dashboard.html integration...")
            await page.locator(".sidebar").get_by_text("Health Monitor").click()
            iframe = page.frame_locator("#health-monitor-page iframe")
            await expect(iframe.locator(".dashboard-header h1")).to_be_visible(timeout=10000)
            await page.screenshot(path="docs/screenshots/03_service_dashboard.png")
            print("✓ Screenshot saved to docs/screenshots/03_service_dashboard.png")

            # 4. Screenshot ai-config-manager.html
            print("\nCapturing screenshot for ai-config-manager.html...")
            await page.goto("http://localhost:9999/ai-config-manager.html", wait_until="load")
            await expect(page.get_by_role("heading", name="AI Config Manager")).to_be_visible()
            await page.screenshot(path="docs/screenshots/04_ai_config_manager.png")
            print("✓ Screenshot saved to docs/screenshots/04_ai_config_manager.png")

            print("\nAll screenshots generated successfully.")

        except Exception as e:
            print(f"An error occurred during screenshot generation: {e}")
            raise e

        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
