#!/usr/bin/env python3
"""
Multi-Source Validation Module

Validates data across multiple sources and computes confidence scores.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ConfidenceLevel(Enum):
    """Confidence level based on source agreement."""
    HIGH = "high"      # 3+ sources agree
    MEDIUM = "medium"  # 2 sources agree
    LOW = "low"       # conflicting or insufficient


@dataclass
class ValidationResult:
    """Result of cross-source validation."""
    score: float
    confidence: ConfidenceLevel
    warnings: list[str] = field(default_factory=list)
    sources_used: list[str] = field(default_factory=list)

    def add_warning(self, warning: str) -> None:
        """Add a warning message to the result."""
        self.warnings.append(warning)

    def add_source(self, source: str) -> None:
        """Add a source to the list of sources used."""
        self.sources_used.append(source)


class CrossValidator:
    """Validates data against multiple sources."""

    def __init__(self, min_confidence_threshold: float = 0.5):
        """
        Initialize validator.

        Args:
            min_confidence_threshold: Minimum score threshold for validation.
        """
        self.min_confidence_threshold = min_confidence_threshold

    def validate(self, data_points: dict[str, Any]) -> ValidationResult:
        """
        Validate data across multiple sources.

        Args:
            data_points: Dict mapping source names to their data values.

        Returns:
            ValidationResult with score, confidence, warnings, and sources.
        """
        warnings = []
        sources = list(data_points.keys())

        if len(sources) < 2:
            warnings.append("Insufficient sources for validation")
            return ValidationResult(
                score=0.0,
                confidence=ConfidenceLevel.LOW,
                warnings=warnings,
                sources_used=sources
            )

        values = list(data_points.values())
        unique_values = set(values)
        agreement_count = len(values) - len(unique_values) + 1

        if agreement_count >= 3:
            confidence = ConfidenceLevel.HIGH
        elif agreement_count == 2:
            confidence = ConfidenceLevel.MEDIUM
        else:
            confidence = ConfidenceLevel.LOW
            warnings.append("Sources have conflicting values")

        score = agreement_count / len(sources)

        return ValidationResult(
            score=score,
            confidence=confidence,
            warnings=warnings,
            sources_used=sources
        )


if __name__ == "__main__":
    validator = CrossValidator()

    sample_data = {
        "source1": "value_a",
        "source2": "value_a",
        "source3": "value_a"
    }

    result = validator.validate(sample_data)
    print(f"Score: {result.score}")
    print(f"Confidence: {result.confidence.value}")
    print(f"Sources: {result.sources_used}")
    print(f"Warnings: {result.warnings}")
