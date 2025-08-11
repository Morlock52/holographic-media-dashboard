import asyncio
from playwright.async_api import async_playwright, expect

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        try:
            await page.goto("http://localhost:9999/ai-config-manager.html", wait_until="load")

            # Check for the main title
            await expect(page.get_by_role("heading", name="AI Config Manager")).to_be_visible()

            # Click the "Generate API Key" button
            generate_button = page.get_by_role("button", name="🔑 Generate API Key")
            await expect(generate_button).to_be_visible()
            await generate_button.click()

            # Wait for the AI assistant to respond
            chat_messages = page.locator("#chatMessages")
            await expect(chat_messages.get_by_text("Generated API key:")).to_be_visible(timeout=5000)

            # Check that a second message about copying to clipboard appears
            await expect(chat_messages.get_by_text("✓ API key copied to clipboard!")).to_be_visible()

            await page.screenshot(path="jules-scratch/verification/ai_config_fixed.png")
            print("Screenshot taken successfully.")

        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
