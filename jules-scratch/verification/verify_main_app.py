import asyncio
from playwright.async_api import async_playwright, expect

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        try:
            await page.goto("http://localhost:9999/main-app.html", wait_until="load")

            # Define the navigation items and their expected iframe sources/pages
            nav_tests = [
                { "nav_text": "Media Library", "page_id": "#media-library-page", "iframe_src": "demo-showcase.html" },
                { "nav_text": "Configuration", "page_id": "#config-manager-page", "iframe_src": "config-manager-fixed.html" },
                { "nav_text": ".env Editor", "page_id": "#env-editor-page", "iframe_src": "smart-env-editor.html" },
                { "nav_text": "Health Monitor", "page_id": "#health-monitor-page", "iframe_src": "service-dashboard.html" },
                { "nav_text": "Documentation", "page_id": "#documentation-page", "iframe_src": "docs/README.md" },
            ]

            for test in nav_tests:
                print(f"Testing navigation to: {test['nav_text']}")

                # Click the navigation item in the sidebar
                await page.locator(".sidebar").get_by_text(test["nav_text"]).click()

                # Find the corresponding page container and check that it's visible
                page_container = page.locator(test["page_id"])
                await expect(page_container).to_be_visible()

                # Check that the iframe within the container has the correct source
                iframe = page_container.locator("iframe")
                await expect(iframe).to_have_attribute("src", test["iframe_src"])

                print(f"✓ Successfully navigated to {test['nav_text']}")

            # Take a final screenshot of the last navigated page
            await page.screenshot(path="jules-scratch/verification/main_app_fixed.png")
            print("\nScreenshot taken successfully.")
            print("Main app navigation verification successful.")

        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
