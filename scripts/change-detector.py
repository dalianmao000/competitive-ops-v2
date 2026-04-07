#!/usr/bin/env python3
"""
Change Detection Module

Detects changes in data (e.g., pricing) against configurable thresholds.
"""

import yaml
from pathlib import Path
from typing import Any, Optional


class ChangeDetector:
    """Detects changes in data based on configured thresholds."""

    def __init__(self, config_path: str):
        """
        Initialize change detector with configuration.

        Args:
            config_path: Path to YAML configuration file.

        Raises:
            FileNotFoundError: If config file doesn't exist.
            yaml.YAMLError: If config file is invalid YAML.
        """
        self.config_path = Path(config_path)
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")

        with open(self.config_path) as f:
            self.config = yaml.safe_load(f)

    def detect_pricing_change(
        self,
        old: dict[str, Any],
        new: dict[str, Any],
        product_key: str = "price"
    ) -> bool:
        """
        Detect if pricing changed beyond configured threshold.

        Args:
            old: Dict containing old pricing data.
            new: Dict containing new pricing data.
            product_key: Key to access pricing value in dicts.

        Returns:
            True if change exceeds threshold, False otherwise.
        """
        thresholds = self.config.get("thresholds", {}).get("pricing", {})
        absolute_threshold = thresholds.get("absolute", 0)
        percentage_threshold = thresholds.get("percentage", 0)

        old_price = old.get(product_key, 0)
        new_price = new.get(product_key, 0)

        if old_price == 0:
            return new_price != 0

        absolute_change = abs(new_price - old_price)
        percentage_change = abs((new_price - old_price) / old_price) * 100

        return (
            absolute_change >= absolute_threshold or
            percentage_change >= percentage_threshold
        )

    def detect_change(
        self,
        old: Any,
        new: Any,
        field: str,
        data_type: str = "numeric"
    ) -> bool:
        """
        Generic change detection for any field.

        Args:
            old: Old data dict.
            new: New data dict.
            field: Field name to check for changes.
            data_type: Type of data ("numeric", "text", "list").

        Returns:
            True if change detected beyond threshold, False otherwise.
        """
        if data_type == "numeric":
            old_val = old.get(field, 0)
            new_val = new.get(field, 0)
            threshold_key = f"{field}_threshold"
            threshold = self.config.get("thresholds", {}).get(threshold_key, 0)

            if old_val == 0:
                return new_val != 0
            return abs(new_val - old_val) >= threshold

        elif data_type == "text":
            return old.get(field) != new.get(field)

        elif data_type == "list":
            old_list = set(old.get(field, []))
            new_list = set(new.get(field, []))
            return old_list != new_list

        return False


if __name__ == "__main__":
    import tempfile
    import os

    config = {
        "thresholds": {
            "pricing": {
                "absolute": 10.0,
                "percentage": 5.0
            }
        }
    }

    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        yaml.dump(config, f)
        config_path = f.name

    try:
        detector = ChangeDetector(config_path)

        old_pricing = {"price": 100.0}
        new_pricing = {"price": 115.0}

        changed = detector.detect_pricing_change(old_pricing, new_pricing)
        print(f"Pricing change detected: {changed}")
    finally:
        os.unlink(config_path)
