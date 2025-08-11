import asyncio
from playwright.async_api import async_playwright, expect

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        console_messages = []
        page.on("console", lambda msg: console_messages.append(f"[{msg.type}] {msg.text}"))

        try:
            await page.goto("http://localhost:9999/media-assistant.html", wait_until="load")

            # Check for the main title inside the chat header
            chat_header = page.locator(".chat-header")
            await expect(chat_header.get_by_role("heading", name="Media Assistant")).to_be_visible()

            # Type a message into the chat input
            chat_input = page.locator("#chatInput")
            await chat_input.fill("Hello")

            # Click the send button
            await page.get_by_role("button", name="Send").click()

            # Wait for the mock response to appear
            chat_messages = page.locator("#chatMessages")
            await expect(chat_messages.get_by_text("This is a mock response")).to_be_visible(timeout=10000)

            await page.screenshot(path="jules-scratch/verification/media_assistant_fixed.png")
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
