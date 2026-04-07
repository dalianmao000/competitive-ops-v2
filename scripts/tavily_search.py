#!/usr/bin/env python3
"""
Tavily Search Integration

Provides company search and news search capabilities using the Tavily API.
"""

import os
from tavily import TavilyClient


class TavilySearch:
    """Tavily API client for company and news searches."""

    def __init__(self, api_key: str = None):
        """
        Initialize Tavily client.

        Args:
            api_key: Tavily API key. If not provided, reads from TAVILY_API_KEY env var.
        """
        self.api_key = api_key or os.getenv("TAVILY_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Tavily API key not provided. Set TAVILY_API_KEY environment variable "
                "or pass api_key parameter."
            )
        self.client = TavilyClient(api_key=self.api_key)

    def search_company(self, company: str) -> dict:
        """
        Search for company information.

        Args:
            company: Company name to search for.

        Returns:
            Dict containing search results with company overview, products, and pricing.
        """
        return self.client.search(
            query=f"{company} company overview products pricing",
            topic="business",
            max_results=10
        )

    def search_news(self, company: str) -> dict:
        """
        Search for recent news about a company.

        Args:
            company: Company name to search for.

        Returns:
            Dict containing recent news results from 2026.
        """
        return self.client.search(
            query=f"{company} news 2026",
            topic="news",
            max_results=5
        )


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: tavily-search.py <company_name>")
        sys.exit(1)

    company = sys.argv[1]
    search = TavilySearch()

    print(f"Searching for company info: {company}")
    result = search.search_company(company)
    print(result)

    print(f"\nSearching for news: {company}")
    news = search.search_news(company)
    print(news)
