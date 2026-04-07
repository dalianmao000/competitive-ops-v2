#!/usr/bin/env python3
"""
i18n - Internationalization module for competitive-ops

Provides translation functionality for reports with support for
English and Chinese languages.
"""

import re
import os
from pathlib import Path
from typing import Dict, Optional


class I18n:
    """Internationalization handler for competitive-ops reports."""

    DEFAULT_LANG = "en"
    SUPPORTED_LANGS = ["en", "zh-CN"]

    def __init__(self, i18n_dir: Optional[str] = None):
        """
        Initialize I18n with the i18n directory.

        Args:
            i18n_dir: Path to the i18n directory. Defaults to project root/i18n.
        """
        if i18n_dir is None:
            # Default to project root/i18n
            self.i18n_dir = Path(__file__).parent.parent / "i18n"
        else:
            self.i18n_dir = Path(i18n_dir)

        self.strings: Dict[str, Dict[str, str]] = {}
        self._load_all_strings()

    def _load_all_strings(self) -> None:
        """Load all strings-*.md files from the i18n directory."""
        if not self.i18n_dir.exists():
            return

        for lang_file in self.i18n_dir.glob("strings-*.md"):
            lang_code = lang_file.stem.replace("strings-", "")
            self.strings[lang_code] = self._parse_strings(lang_file)

    def _parse_strings(self, path: Path) -> Dict[str, str]:
        """
        Parse a markdown table file into a key-value dictionary.

        Args:
            path: Path to the strings-*.md file.

        Returns:
            Dictionary of key-value translations.
        """
        result = {}
        content = path.read_text(encoding="utf-8")

        # Parse markdown table: | key | value |
        # Skip header and separator lines
        lines = content.split("\n")
        for line in lines:
            line = line.strip()
            if not line or line.startswith("#") or line.startswith("|" + "---"):
                continue
            if line.startswith("|"):
                parts = [p.strip() for p in line.split("|")]
                # parts[0] is empty, parts[1] is key, parts[2] is value
                if len(parts) >= 3:
                    key = parts[1]
                    value = parts[2]
                    if key and value:
                        result[key] = value

        return result

    def detect_language(
        self, config_lang: Optional[str] = None, accept_language: Optional[str] = None
    ) -> str:
        """
        Detect the appropriate language based on config and Accept-Language header.

        Priority:
        1. config_lang (from config/profile.yml)
        2. accept_language (from HTTP Accept-Language header)
        3. default (en)

        Args:
            config_lang: Language from config file.
            accept_language: Language from Accept-Language header.

        Returns:
            Language code (en or zh-CN).
        """
        # Priority 1: config setting
        if config_lang and config_lang in self.SUPPORTED_LANGS:
            return config_lang

        # Priority 2: Accept-Language header
        if accept_language:
            # Parse Accept-Language header (e.g., "zh-CN,zh;q=0.9,en;q=0.8")
            langs = self._parse_accept_language(accept_language)
            for lang in langs:
                if lang in self.SUPPORTED_LANGS:
                    return lang

        # Priority 3: default
        return self.DEFAULT_LANG

    def _parse_accept_language(self, accept_language: str) -> list:
        """
        Parse Accept-Language header into ordered list of language codes.

        Args:
            accept_language: Raw Accept-Language header value.

        Returns:
            List of language codes in priority order.
        """
        result = []
        parts = accept_language.split(",")

        lang_weights = []
        for part in parts:
            part = part.strip()
            if ";" in part:
                lang, weight = part.split(";")
                lang = lang.strip()
                # Extract q value
                q_match = re.search(r"q=([0-9.]+)", weight)
                q = float(q_match.group(1)) if q_match else 1.0
            else:
                lang = part
                q = 1.0

            # Normalize language code
            lang = lang.replace("_", "-")
            lang_weights.append((lang, q))

        # Sort by weight descending
        lang_weights.sort(key=lambda x: x[1], reverse=True)

        for lang, _ in lang_weights:
            # Handle wildcards
            if lang == "*":
                continue
            result.append(lang)

            # Handle primary language (e.g., "zh" matches "zh-CN")
            primary = lang.split("-")[0]
            if primary != lang and primary not in result:
                # Check if we have a specific variant
                for supported in self.SUPPORTED_LANGS:
                    if supported.startswith(primary):
                        result.append(supported)

        return result

    def t(self, key: str, lang: Optional[str] = None) -> str:
        """
        Get translation for a key.

        Args:
            key: Translation key (e.g., "report.title").
            lang: Language code. If None, uses default.

        Returns:
            Translated string, or the key itself if not found.
        """
        if lang is None:
            lang = self.DEFAULT_LANG

        if lang not in self.strings:
            return key

        return self.strings[lang].get(key, key)

    def t_template(self, template: str, lang: Optional[str] = None) -> str:
        """
        Replace {key} placeholders in a template with translations.

        Args:
            template: Template string with {key} placeholders.
            lang: Language code. If None, uses default.

        Returns:
            Template with placeholders replaced by translations.
        """
        if lang is None:
            lang = self.DEFAULT_LANG

        def replace_placeholder(match):
            key = match.group(1)
            return self.t(key, lang)

        # Replace {key} patterns
        return re.sub(r"\{([^}]+)\}", replace_placeholder, template)

    def get_all_keys(self, lang: Optional[str] = None) -> list:
        """
        Get all available translation keys for a language.

        Args:
            lang: Language code. If None, uses default.

        Returns:
            List of all translation keys.
        """
        if lang is None:
            lang = self.DEFAULT_LANG

        if lang not in self.strings:
            return []

        return list(self.strings[lang].keys())


# Module-level convenience functions
_instance: Optional[I18n] = None


def _get_instance() -> I18n:
    """Get or create the global I18n instance."""
    global _instance
    if _instance is None:
        _instance = I18n()
    return _instance


def t(key: str, lang: Optional[str] = None) -> str:
    """Convenience function for translations."""
    return _get_instance().t(key, lang)


def t_template(template: str, lang: Optional[str] = None) -> str:
    """Convenience function for template translations."""
    return _get_instance().t_template(template, lang)


def detect_language(
    config_lang: Optional[str] = None, accept_language: Optional[str] = None
) -> str:
    """Convenience function for language detection."""
    return _get_instance().detect_language(config_lang, accept_language)


if __name__ == "__main__":
    # Test the module
    i18n = I18n()
    print(f"Loaded languages: {list(i18n.strings.keys())}")
    print(f"Sample translations (en):")
    print(f"  report.title = {i18n.t('report.title', 'en')}")
    print(f"  swot.strengths = {i18n.t('swot.strengths', 'en')}")
    print(f"Sample translations (zh-CN):")
    print(f"  report.title = {i18n.t('report.title', 'zh-CN')}")
    print(f"  swot.strengths = {i18n.t('swot.strengths', 'zh-CN')}")
    print(f"Template example:")
    print(f"  {i18n.t_template('executive_summary.period_theme', 'en')}")
    print(f"  (with {{month}}='April'): {i18n.t_template('executive_summary.period_theme', 'en').replace('{month}', 'April')}")
