import asyncio
from playwright.async_api import async_playwright, expect

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        console_messages = []
        page.on("console", lambda msg: console_messages.append(f"[{msg.type}] {msg.text}"))

        try:
            await page.goto("http://localhost:9999/demo-showcase.html", wait_until="networkidle")

            # Check for the main title
            await expect(page.get_by_role("heading", name="HoloMedia Hub")).to_be_visible()

            # Verify the "Agentic Workflows" button is now a button and not a link
            open_builder_button = page.locator(".component-card", has_text="Agentic Workflows").get_by_text("Open Builder")
            await expect(open_builder_button).to_have_attribute("onclick", "alert('This feature is not yet available.')")

            # Verify the "Documentation" link has the correct href
            view_docs_link = page.locator(".component-card", has_text="Documentation").get_by_role("link", name="View Docs")
            await expect(view_docs_link).to_have_attribute("href", "docs/README.md")

            await page.screenshot(path="jules-scratch/verification/showcase_fixed.png")
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
