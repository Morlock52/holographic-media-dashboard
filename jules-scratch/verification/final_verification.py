import asyncio
from playwright.async_api import async_playwright, expect

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        try:
            # 1. Verify main-app.html shell
            print("Verifying main-app.html shell...")
            await page.goto("http://localhost:9999/main-app.html", wait_until="load")
            await expect(page.locator(".sidebar")).to_be_visible()
            await page.screenshot(path="jules-scratch/verification/01_main_app_shell.png")
            print("✓ main-app.html shell verified.")

            # 2. Verify navigation to the fixed service-dashboard
            print("\nVerifying navigation to service-dashboard.html...")
            await page.locator(".sidebar").get_by_text("Health Monitor").click()

            # The page is inside an iframe
            iframe = page.frame_locator("#health-monitor-page iframe")
            # Be more specific with the locator to avoid strict mode violation
            await expect(iframe.locator(".dashboard-header h1")).to_be_visible(timeout=10000)
            await expect(iframe.locator("#servicesGrid").get_by_text("Jellyfin")).to_be_visible()

            await page.screenshot(path="jules-scratch/verification/02_service_dashboard_integration.png")
            print("✓ service-dashboard.html integration verified.")

            # 3. Verify the standalone ai-config-manager
            print("\nVerifying ai-config-manager.html...")
            await page.goto("http://localhost:9999/ai-config-manager.html", wait_until="load")
            await expect(page.get_by_role("heading", name="AI Config Manager")).to_be_visible()
            await page.get_by_role("button", name="🔑 Generate API Key").click()
            await expect(page.locator("#chatMessages").get_by_text("Generated API key:")).to_be_visible(timeout=5000)

            await page.screenshot(path="jules-scratch/verification/03_ai_config_manager.png")
            print("✓ ai-config-manager.html verified.")

            print("\nFinal verification complete.")

        except Exception as e:
            print(f"An error occurred during final verification: {e}")
            # Still try to close browser
            await browser.close()
            # Re-raise the exception so the process exits with an error
            raise e

        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
