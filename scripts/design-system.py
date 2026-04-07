#!/usr/bin/env python3
"""
UI-UX Pro Max Integration

Queries the ui-ux-pro-max design system recommendations.
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Optional


def get_design_system(
    product_type: str,
    style: Optional[str] = None,
    ui_ux_script_path: str = "src/ui-ux-pro-max/scripts/search.py"
) -> dict:
    """
    Query ui-ux-pro-max for design system recommendations.

    Args:
        product_type: Type of product to get design recommendations for.
        style: Optional style preference (e.g., "modern", "minimal").
        ui_ux_script_path: Path to the ui-ux-pro-max search script.

    Returns:
        Dict containing design system recommendations.

    Raises:
        FileNotFoundError: If the ui-ux-pro-max script doesn't exist.
        subprocess.CalledProcessError: If the script execution fails.
    """
    script_path = Path(ui_ux_script_path)
    if not script_path.exists():
        raise FileNotFoundError(
            f"ui-ux-pro-max script not found at: {ui_ux_script_path}. "
            "Please ensure ui-ux-pro-max is installed or provide correct path."
        )

    cmd = [
        "python3",
        str(script_path),
        product_type,
        "--domain", "style"
    ]

    if style:
        cmd.extend(["--style", style])

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout)

    except subprocess.CalledProcessError as e:
        print(f"Error running ui-ux-pro-max: {e.stderr}", file=sys.stderr)
        raise
    except json.JSONDecodeError as e:
        print(f"Error parsing ui-ux-pro-max output: {e}", file=sys.stderr)
        raise


def get_color_palette(product_type: str) -> dict:
    """Get recommended color palette for a product type."""
    result = get_design_system(product_type)
    return result.get("colors", {})


def get_typography(product_type: str) -> dict:
    """Get recommended typography for a product type."""
    result = get_design_system(product_type)
    return result.get("typography", {})


def get_component_library(product_type: str) -> dict:
    """Get recommended component library for a product type."""
    result = get_design_system(product_type)
    return result.get("components", {})


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: design-system.py <product_type> [--style <style>]")
        sys.exit(1)

    product_type = sys.argv[1]
    style = None

    if len(sys.argv) >= 4 and sys.argv[2] == "--style":
        style = sys.argv[3]

    try:
        result = get_design_system(product_type, style)
        print(json.dumps(result, indent=2))
    except FileNotFoundError as e:
        print(f"Setup required: {e}", file=sys.stderr)
        print("Returning mock design system data...")
        mock_result = {
            "product_type": product_type,
            "style": style or "default",
            "colors": {"primary": "#007bff", "secondary": "#6c757d"},
            "typography": {"heading": "Inter", "body": "Roboto"},
            "components": ["button", "input", "card"]
        }
        print(json.dumps(mock_result, indent=2))
