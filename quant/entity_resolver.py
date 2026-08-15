"""
Athena Asset Entity Resolver

Resolves natural-language asset references into
validated market ticker symbols.

Resolution strategy:

1. Known aliases
2. Explicit ticker symbols / cashtags
3. Alpaca's active US-equity asset universe

The resolver performs identification only.
It does not perform market analysis.
"""

import os
import re
from functools import lru_cache

from dotenv import load_dotenv

from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetAssetsRequest
from alpaca.trading.enums import (
    AssetClass,
    AssetStatus,
)


load_dotenv()


# ---------------------------------------------------------
# Common aliases
# ---------------------------------------------------------

# Small convenience layer for recognizable brand names
# or common company references.
#
# This is not the primary source of asset resolution.

COMMON_ALIASES = {
    "apple": "AAPL",
    "nvidia": "NVDA",
    "microsoft": "MSFT",
    "tesla": "TSLA",
    "google": "GOOGL",
    "facebook": "META",
    "jp morgan": "JPM",
    "jpmorgan": "JPM",
    "spy": "SPY",
    "qqq": "QQQ",
}


# ---------------------------------------------------------
# Reserved ticker words
# ---------------------------------------------------------

# Uppercase words that may legitimately appear in normal
# quantitative language and should not automatically be
# interpreted as ticker symbols.

RESERVED_TICKER_WORDS = {
    "AI",
    "API",
    "ATHENA",
    "ES",
    "ETF",
    "GDP",
    "LLM",
    "MAX",
    "MIN",
    "PDF",
    "USD",
    "VAR",
}


# ---------------------------------------------------------
# Ambiguous natural-language words
# ---------------------------------------------------------

# These words are unsafe as standalone company-name
# matches because they frequently occur in ordinary
# research requests.
#
# Full company phrases remain valid.
#
# Example:
#
# "five years"
#     -> NOT an asset
#
# "Five Below"
#     -> FIVE
#
# "FIVE"
#     -> FIVE when explicitly written as a ticker

AMBIGUOUS_SINGLE_WORDS = {
    # Generic company-name words
    "american",
    "bank",
    "capital",
    "first",
    "general",
    "global",
    "national",
    # Natural-language question words
    "where",
    "which",
    "what",
    "when",
    "why",
    "how",
    "new",
    "united",
    "us",

    # Number words
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
    "ten",
    "eleven",
    "twelve",

    # Time language
    "day",
    "days",
    "week",
    "weeks",
    "month",
    "months",
    "year",
    "years",

    # Common quantitative language
    "risk",
    "return",
    "returns",
    "value",
    "average",
    "market",
    "stock",
    "equity",
    "price",
    "growth",
    "income",
    "financial",
    "investment",
    "monte",
    "carlo",
    "simulation",
    "simulations",
    "simulate",
    "next",
    "forward",
    "future",
    "run",
    "investments",
    "portfolio",
    "simulation",
    "analysis",
    "research",
}


def _normalize_text(value: str) -> str:
    """
    Normalize text for company-name matching.
    """

    value = value.lower()

    value = value.replace(
        "&",
        " and ",
    )

    value = re.sub(
        r"[^a-z0-9]+",
        " ",
        value,
    )

    return " ".join(
        value.split()
    )


def _clean_company_name(name: str) -> str:
    """
    Reduce an Alpaca security name to its
    recognizable company-name core.

    Examples:

    Apple Inc
        -> apple

    Amazon.com Inc
        -> amazon

    Alphabet Inc Class A
        -> alphabet
    """

    name = _normalize_text(
        name
    )

    # Remove share-class descriptions.

    name = re.sub(
        r"\bclass\s+[a-z]\b$",
        "",
        name,
    ).strip()

    name = re.sub(
        r"\bcommon stock\b$",
        "",
        name,
    ).strip()

    name = re.sub(
        r"\bordinary shares?\b$",
        "",
        name,
    ).strip()

    # Remove common legal suffixes.

    suffix_pattern = (
        r"\b("
        r"incorporated|"
        r"inc|"
        r"corporation|"
        r"corp|"
        r"company|"
        r"co|"
        r"limited|"
        r"ltd|"
        r"plc|"
        r"holdings?|"
        r"group"
        r")\b$"
    )

    previous = None

    while name and name != previous:

        previous = name

        name = re.sub(
            suffix_pattern,
            "",
            name,
        ).strip()

    # Amazon.com -> amazon

    name = re.sub(
        r"\bcom$",
        "",
        name,
    ).strip()

    return name


@lru_cache(maxsize=1)
def _load_asset_universe():
    """
    Retrieve and cache Alpaca's active
    US-equity asset universe.

    The API is contacted only once per
    Athena process.
    """

    client = TradingClient(
        os.environ["ALPACA_API_KEY"],
        os.environ["ALPACA_SECRET_KEY"],
        paper=True,
    )

    request = GetAssetsRequest(
        status=AssetStatus.ACTIVE,
        asset_class=AssetClass.US_EQUITY,
    )

    return client.get_all_assets(
        request
    )


def _is_safe_single_word(
    word: str,
) -> bool:
    """
    Determine whether a company-name word is
    distinctive enough to use as a standalone
    natural-language asset reference.
    """

    if len(word) < 4:
        return False

    if word in AMBIGUOUS_SINGLE_WORDS:
        return False

    if word.isdigit():
        return False

    return True


def _build_company_phrases(
    company_name: str,
) -> list[str]:
    """
    Build safe natural-language phrases
    for matching a company name.

    Full company names and useful multi-word
    prefixes are allowed.

    A single first word is allowed only when
    it is distinctive enough to avoid common
    natural-language collisions.
    """

    company_name = _clean_company_name(
        company_name
    )

    if not company_name:
        return []

    words = company_name.split()

    phrases = [
        company_name
    ]

    # Multi-word prefixes are substantially safer
    # than standalone generic first words.
    #
    # Examples:
    #   Five Below
    #   General Motors
    #   Bank of America

    if len(words) >= 2:

        first_two = " ".join(
            words[:2]
        )

        if len(first_two) >= 6:
            phrases.append(
                first_two
            )

    # Distinctive first-word company references.
    #
    # Examples:
    #   Palantir Technologies -> palantir
    #   JPMorgan Chase -> jpmorgan
    #
    # Ambiguous words such as "five" are rejected.

    first_word = words[0]

    if _is_safe_single_word(
        first_word
    ):
        phrases.append(
            first_word
        )

    return list(
        dict.fromkeys(
            phrases
        )
    )


def _find_phrase(
    normalized_text: str,
    phrase: str,
) -> int | None:
    """
    Find a complete normalized phrase
    inside normalized user text.
    """

    pattern = (
        r"(?<![a-z0-9])"
        + re.escape(phrase)
        + r"(?![a-z0-9])"
    )

    match = re.search(
        pattern,
        normalized_text,
    )

    if match:
        return match.start()

    return None


def _explicit_ticker_candidates(
    text: str,
) -> list[tuple[int, str]]:
    """
    Extract explicit ticker-like references.

    Supports:

    PLTR
    AMD
    $PLTR
    $nvda
    BRK.B
    """

    candidates = []

    pattern = re.compile(
        r"\$([A-Za-z]{1,5}(?:\.[A-Za-z])?)"
        r"|"
        r"\b([A-Z]{1,5}(?:\.[A-Z])?)\b"
    )

    for match in pattern.finditer(
        text
    ):

        raw_symbol = (
            match.group(1)
            or match.group(2)
        )

        symbol = raw_symbol.upper()

        if symbol in RESERVED_TICKER_WORDS:
            continue

        candidates.append(
            (
                match.start(),
                symbol,
            )
        )

    return candidates


def resolve_assets(
    text: str,
) -> list[str]:
    """
    Resolve asset references from natural language.

    Examples:

    "Analyze Nvidia risk"
        -> ["NVDA"]

    "Compare Amazon and JPMorgan"
        -> ["AMZN", "JPM"]

    "Analyze PLTR and AMD"
        -> ["PLTR", "AMD"]

    "Compare $aapl and $nvda"
        -> ["AAPL", "NVDA"]

    "Analyze Nvidia over five years"
        -> ["NVDA"]

    "Analyze Five Below"
        -> ["FIVE"]
    """

    normalized_text = _normalize_text(
        text
    )

    matches = []

    # -----------------------------------------------------
    # Known aliases
    # -----------------------------------------------------

    for name, ticker in COMMON_ALIASES.items():

        position = _find_phrase(
            normalized_text,
            _normalize_text(name),
        )

        if position is not None:

            matches.append(
                (
                    position,
                    ticker,
                )
            )

    # -----------------------------------------------------
    # Load Alpaca asset universe
    # -----------------------------------------------------

    try:

        assets = _load_asset_universe()

        symbol_map = {
            asset.symbol.upper(): asset
            for asset in assets
        }

    except Exception:

        # Athena can still resolve known aliases and
        # explicit ticker syntax if the asset directory
        # is temporarily unavailable.

        assets = []

        symbol_map = {}

    # -----------------------------------------------------
    # Explicit ticker symbols
    # -----------------------------------------------------

    explicit_candidates = (
        _explicit_ticker_candidates(
            text
        )
    )

    for position, ticker in explicit_candidates:

        if (
            not symbol_map
            or ticker in symbol_map
        ):

            matches.append(
                (
                    position,
                    ticker,
                )
            )

    # -----------------------------------------------------
    # Alpaca company-name matching
    # -----------------------------------------------------

    for asset in assets:

        if not asset.name:
            continue

        ticker = asset.symbol.upper()

        phrases = _build_company_phrases(
            asset.name
        )

        best_position = None

        for phrase in phrases:

            position = _find_phrase(
                normalized_text,
                phrase,
            )

            if position is not None:

                if (
                    best_position is None
                    or position < best_position
                ):
                    best_position = position

        if best_position is not None:

            matches.append(
                (
                    best_position,
                    ticker,
                )
            )

    # -----------------------------------------------------
    # Preserve mention order and remove duplicates
    # -----------------------------------------------------

    matches.sort(
        key=lambda item: item[0]
    )

    resolved = []

    seen = set()

    for _, ticker in matches:

        if ticker not in seen:

            seen.add(
                ticker
            )

            resolved.append(
                ticker
            )

    return resolved