# scripts/test_browser.py
import asyncio
from playwright.async_api import async_playwright
import os
import shutil

async def main():
    print("🔍 Checking for Playwright browser path...")

    # Path ที่ใช้สำหรับ playwright cache
    browser_cache = os.path.expanduser("~/.cache/ms-playwright")
    if os.path.exists(browser_cache):
        print(f"✅ Browser cache exists at: {browser_cache}")
    else:
        print("❌ Browser cache not found. Playwright may not be installed correctly.")

    print("🚀 Launching Chromium...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://example.com")
        await page.screenshot(path="example.png")
        print("📷 Screenshot saved to 'example.png'")
        await browser.close()
        print("✅ Browser launched and closed successfully.")

if __name__ == "__main__":
    asyncio.run(main())
