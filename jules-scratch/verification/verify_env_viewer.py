import asyncio
from playwright.async_api import async_playwright, expect

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        console_messages = []
        page.on("console", lambda msg: console_messages.append(f"[{msg.type}] {msg.text}"))

        try:
            await page.goto("http://localhost:9999/env-viewer.html", wait_until="networkidle")

            # Check for the main title in the header component
            header_title = page.locator("navigation-header")
            await expect(header_title).to_be_visible()
            await expect(header_title).to_contain_text(".env Configuration Viewer")

            # Check for the updated instructions text
            instructions = page.locator(".instructions")
            await expect(instructions).to_contain_text("cd /path/to/your/project")

            # Check for raw .env content
            env_content = page.locator("#envContent")
            await expect(env_content.get_by_text("PUID=1000")).to_be_visible()

            # Check for parsed variable in the grid
            value_grid = page.locator("#valueGrid")
            puid_item = value_grid.locator(".value-item", has_text="PUID")
            await expect(puid_item).to_be_visible()

            await page.screenshot(path="jules-scratch/verification/env_viewer_fixed.png")
            print("Screenshot taken successfully.")

        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            print("\n--- Console Messages ---")
            if console_messages:
                for msg in console_messages:
                    print(msg)
            else:
                print("No console messages were captured.")
            print("------------------------\n")

            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
