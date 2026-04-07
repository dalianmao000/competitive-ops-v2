#!/usr/bin/env python3
"""
Playwright Screenshot Utility

Captures screenshots of URLs using Playwright browser automation.
"""

import asyncio
import sys
from pathlib import Path
from typing import Optional

from playwright.async_api import async_playwright, Playwright


async def capture_screenshot(
    url: str,
    output_path: str,
    full_page: bool = True,
    timeout: int = 30000
) -> bool:
    """
    Capture screenshot of a URL.

    Args:
        url: URL to navigate to and capture.
        output_path: Path where the screenshot should be saved.
        full_page: If True, capture the entire scrollable page.
        timeout: Navigation timeout in milliseconds.

    Returns:
        True if screenshot was captured successfully, False otherwise.
    """
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()

            await page.goto(url, timeout=timeout)
            await page.wait_for_load_state("networkidle")

            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            await page.screenshot(path=output_path, full_page=full_page)

            await browser.close()
            return True

    except Exception as e:
        print(f"Error capturing screenshot: {e}", file=sys.stderr)
        return False


async def capture_screenshots(urls: list[str], output_dir: str) -> dict[str, bool]:
    """
    Capture screenshots of multiple URLs.

    Args:
        urls: List of URLs to capture.
        output_dir: Directory to save screenshots.

    Returns:
        Dict mapping URLs to success status.
    """
    results = {}
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        for i, url in enumerate(urls):
            try:
                filename = f"screenshot_{i+1}_{hash(url)}.png"
                filepath = output_path / filename

                await page.goto(url, timeout=30000)
                await page.wait_for_load_state("networkidle")
                await page.screenshot(path=str(filepath), full_page=True)

                results[url] = True
            except Exception as e:
                print(f"Error capturing {url}: {e}", file=sys.stderr)
                results[url] = False

        await browser.close()

    return results


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: screenshot.py <url> <output_path>")
        sys.exit(1)

    url = sys.argv[1]
    output_path = sys.argv[2]

    success = asyncio.run(capture_screenshot(url, output_path))
    sys.exit(0 if success else 1)
