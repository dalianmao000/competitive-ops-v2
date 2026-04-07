#!/usr/bin/env python3
"""
PDF Generation Module

Generates PDF documents from HTML using Puppeteer (Node.js).
"""

import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Optional


def generate_pdf(
    html_path: str,
    output_path: str,
    puppeteer_script: Optional[str] = None
) -> bool:
    """
    Generate PDF from HTML using Puppeteer.

    Args:
        html_path: Path to the HTML file to convert.
        output_path: Path where the PDF should be saved.
        puppeteer_script: Optional path to custom Puppeteer conversion script.

    Returns:
        True if PDF generated successfully, False otherwise.
    """
    html_file = Path(html_path)
    if not html_file.exists():
        print(f"HTML file not found: {html_path}", file=sys.stderr)
        return False

    if puppeteer_script is None:
        puppeteer_script = str(Path(__file__).parent / "puppeteer-pdf.js")

    if not Path(puppeteer_script).exists():
        print(
            f"Puppeteer script not found: {puppeteer_script}. "
            "Please provide a valid path or install the default script.",
            file=sys.stderr
        )
        return False

    try:
        result = subprocess.run(
            ["node", puppeteer_script, html_path, output_path],
            capture_output=True,
            text=True,
            check=True
        )
        return True

    except subprocess.CalledProcessError as e:
        print(f"Error generating PDF: {e.stderr}", file=sys.stderr)
        return False


def generate_pdf_with_options(
    html_path: str,
    output_path: str,
    options: dict
) -> bool:
    """
    Generate PDF with custom options.

    Args:
        html_path: Path to HTML file.
        output_path: Path for output PDF.
        options: Dict with Puppeteer PDF options (format, landscape, etc.).

    Returns:
        True if successful, False otherwise.
    """
    options_json = tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".json",
        delete=False
    )

    try:
        import json
        json.dump(options, options_json)
        options_json.close()

        html_file = Path(html_path)
        if not html_file.exists():
            return False

        result = subprocess.run(
            [
                "node",
                "-e",
                f"""
                const puppeteer = require('puppeteer');
                const options = require('{options_json.name}');
                (async () => {{
                    const browser = await puppeteer.launch();
                    const page = await browser.newPage();
                    await page.goto('file://{html_file.absolute()}');
                    await page.pdf({{ ...options, path: '{output_path}' }});
                    await browser.close();
                }})();
                """
            ],
            capture_output=True,
            text=True
        )

        return result.returncode == 0

    finally:
        Path(options_json.name).unlink(missing_ok=True)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: generate-pdf.py <html_path> <output_path>")
        sys.exit(1)

    html_path = sys.argv[1]
    output_path = sys.argv[2]

    success = generate_pdf(html_path, output_path)
    sys.exit(0 if success else 1)
