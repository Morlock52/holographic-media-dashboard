import asyncio
from playwright.async_api import async_playwright, expect

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={ 'width': 1280, 'height': 800 })
        page = await context.new_page()

        try:
            # 1. Screenshot service-dashboard.html
            print("Capturing screenshot for service-dashboard.html...")
            await page.goto("http://localhost:9999/service-dashboard.html", wait_until="load")
            await expect(page.locator(".dashboard-header h1")).to_be_visible(timeout=10000)
            await page.screenshot(path="docs/screenshots/03_service_dashboard.png")
            print("✓ Screenshot saved to docs/screenshots/03_service_dashboard.png")

            # 2. Screenshot ai-config-manager.html
            print("\nCapturing screenshot for ai-config-manager.html...")
            await page.goto("http://localhost:9999/ai-config-manager.html", wait_until="load")
            await expect(page.get_by_role("heading", name="AI Config Manager")).to_be_visible()
            await page.screenshot(path="docs/screenshots/04_ai_config_manager.png")
            print("✓ Screenshot saved to docs/screenshots/04_ai_config_manager.png")

            print("\nRemaining screenshots generated successfully.")

        except Exception as e:
            print(f"An error occurred during screenshot generation: {e}")
            raise e

        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
