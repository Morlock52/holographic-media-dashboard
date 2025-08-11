import asyncio
from playwright.async_api import async_playwright, expect

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        try:
            await page.goto("http://localhost:9999/config-manager-fixed.html", wait_until="load")

            # Check for the main title in the navigation header
            nav_header = page.locator("navigation-header")
            await expect(nav_header).to_be_visible()
            await expect(nav_header.get_by_text("Configuration Manager")).to_be_visible()

            # The "Environment Variables" tab is active by default
            env_tab = page.locator("#env-tab")
            await expect(env_tab).to_be_visible()

            # Click the "Docker Services" tab
            services_tab_button = page.get_by_text("🐳 Docker Services")
            await services_tab_button.click()

            # Check that the services tab content is now visible
            services_tab_content = page.locator("#services-tab")
            await expect(services_tab_content).to_be_visible()

            # Check that a service card is visible
            jellyfin_card = services_tab_content.locator(".service-card[data-service='jellyfin']")
            await expect(jellyfin_card).to_be_visible()

            await page.screenshot(path="jules-scratch/verification/config_manager_fixed_baseline.png")
            print("Screenshot taken successfully.")

        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
