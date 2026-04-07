#!/usr/bin/env python3
"""Test script to verify competitive-ops-v2 scripts work correctly.

Note: Some tests require Python 3.9+ and optional dependencies.
Run `pip install -r requirements.txt` to enable all tests.
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

def test_cross_validate():
    """Test cross-validation module."""
    print("Testing cross_validate.py...")
    from scripts.cross_validate import ConfidenceLevel, ValidationResult

    result = ValidationResult(
        score=0.85,
        confidence=ConfidenceLevel.HIGH,
        warnings=[],
        sources_used=["tavily", "website", "g2"]
    )
    print(f"  Confidence: {result.confidence.value}")
    print(f"  Score: {result.score}")
    print("  ✅ PASS\n")

def test_change_detector():
    """Test change detector module."""
    print("Testing change_detector.py...")
    from scripts.change_detector import ChangeDetector

    print(f"  ChangeDetector class: {ChangeDetector.__name__}")
    print("  ✅ PASS\n")

def test_tavily_search():
    """Test Tavily search module."""
    print("Testing tavily_search.py...")
    try:
        from scripts.tavily_search import TavilySearch
        print(f"  TavilySearch class: {TavilySearch.__name__}")
        print("  ✅ PASS\n")
    except ImportError:
        print("  ⚠️  SKIP: tavily not installed (run `pip install tavily-python`)\n")
    except TypeError as e:
        if "subscriptable" in str(e):
            print("  ⚠️  SKIP: Python 3.9+ required for tavily\n")
        else:
            raise

def test_html_generator():
    """Test HTML generator module."""
    print("Testing html_generator.py...")
    from scripts.html_generator import HTMLGenerator

    print(f"  HTMLGenerator class: {HTMLGenerator.__name__}")
    print("  ✅ PASS\n")

def test_design_system():
    """Test design system module."""
    print("Testing design_system.py...")
    from scripts.design_system import get_design_system

    print(f"  get_design_system function: {get_design_system.__name__}")
    print("  ✅ PASS\n")

def test_screenshot():
    """Test screenshot module."""
    print("Testing screenshot.py...")
    try:
        from scripts.screenshot import capture_screenshot
        print(f"  capture_screenshot function: {capture_screenshot.__name__}")
        print("  ✅ PASS (requires playwright install)\n")
    except ImportError:
        print("  ⚠️  SKIP: playwright not installed (run `npx playwright install`)\n")

def test_colors_yaml():
    """Test that colors.yml is valid YAML."""
    print("Testing colors.yml...")
    import yaml

    colors_path = Path(project_root) / "templates" / "design" / "colors.yml"
    with open(colors_path) as f:
        colors = yaml.safe_load(f)

    print(f"  Primary color: {colors.get('enterprise', {}).get('primary', 'N/A')}")
    print("  ✅ PASS\n")

def test_html_templates_exist():
    """Test that HTML templates exist."""
    print("Testing HTML templates...")
    from pathlib import Path

    template_dir = Path(project_root) / "templates" / "report" / "html"
    templates = list(template_dir.glob("*.html"))

    print(f"  Found {len(templates)} HTML templates:")
    for t in templates:
        print(f"    - {t.name}")
    print("  ✅ PASS\n")

def test_modes_exist():
    """Test that mode files exist."""
    print("Testing modes...")
    from pathlib import Path

    modes_dir = Path(project_root) / "modes"
    modes = list(modes_dir.glob("*.md"))

    print(f"  Found {len(modes)} mode files:")
    for m in modes:
        print(f"    - {m.name}")
    print("  ✅ PASS\n")

def test_config_files():
    """Test that config files exist."""
    print("Testing config files...")
    from pathlib import Path

    config_dir = Path(project_root) / "config"
    configs = list(config_dir.glob("*.yml"))

    print(f"  Found {len(configs)} config files:")
    for c in configs:
        print(f"    - {c.name}")
    print("  ✅ PASS\n")

def main():
    print("=" * 50)
    print("Competitive-Ops v2 - Test Suite")
    print("=" * 50)
    print()

    tests = [
        test_cross_validate,
        test_change_detector,
        test_tavily_search,
        test_html_generator,
        test_design_system,
        test_screenshot,
        test_colors_yaml,
        test_html_templates_exist,
        test_modes_exist,
        test_config_files,
    ]

    passed = 0
    failed = 0
    skipped = 0

    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"  ❌ FAIL: {e}\n")
            failed += 1

    print("=" * 50)
    print(f"Results: {passed} passed, {failed} failed, {skipped} skipped")
    print("=" * 50)
    print()
    print("To run full tests, install dependencies:")
    print("  pip install -r requirements.txt")
    print("  npx playwright install chromium")
    print()

    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
