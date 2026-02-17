#!/usr/bin/env python3
"""
Fixed Income Dashboard - Data Updater
Fetches current ETF prices, yields, and AUM from Yahoo Finance.
SEC yields and duration are maintained in static config since they
update monthly (not available via free APIs in real-time).
"""

import json
import os
import sys
from datetime import datetime, timezone

try:
    import yfinance as yf
except ImportError:
    print("Installing yfinance...")
    os.system(f"{sys.executable} -m pip install yfinance -q")
    import yfinance as yf


# Static product config - SEC yields, duration, expense ratios updated manually
# These update monthly (SEC yield) or annually (expense ratio)
PRODUCTS = [
    # === TREASURY === (fallback prices from Feb 2026 QC)
    {"ticker": "SGOV", "name": "iShares 0-3 Month Treasury Bond", "type": "treasury", "stateExempt": True,
     "sec_yield": 4.20, "duration": 0.05, "expense": 0.09, "fallback_price": 100.52, "fallback_aum": "70.9B"},
    {"ticker": "BIL", "name": "SPDR Bloomberg 1-3 Month T-Bill", "type": "treasury", "stateExempt": True,
     "sec_yield": 4.19, "duration": 0.13, "expense": 0.14, "fallback_price": 91.51, "fallback_aum": "43.7B"},
    {"ticker": "SHV", "name": "iShares Short Treasury Bond", "type": "treasury", "stateExempt": True,
     "sec_yield": 4.17, "duration": 0.27, "expense": 0.15, "fallback_price": 110.19, "fallback_aum": "22.1B"},
    {"ticker": "GBIL", "name": "Goldman Sachs Access Treasury 0-1 Year", "type": "treasury", "stateExempt": True,
     "sec_yield": 4.20, "duration": 0.25, "expense": 0.12, "fallback_price": 100.04, "fallback_aum": "7.1B"},
    {"ticker": "SCHO", "name": "Schwab Short-Term U.S. Treasury ETF", "type": "treasury", "stateExempt": True,
     "sec_yield": 3.57, "duration": 1.90, "expense": 0.03, "fallback_price": 48.85, "fallback_aum": "10.2B"},
    {"ticker": "XONE", "name": "BondBloxx Bloomberg One Year Treasury", "type": "treasury", "stateExempt": True,
     "sec_yield": 4.05, "duration": 0.95, "expense": 0.03, "fallback_price": 49.56, "fallback_aum": "1.2B"},
    {"ticker": "FTSD", "name": "Franklin Short Duration U.S. Govt ETF", "type": "treasury", "stateExempt": True,
     "sec_yield": 4.15, "duration": 0.65, "expense": 0.25, "fallback_price": 90.95, "fallback_aum": "260M"},
    # === FLOATING RATE ===
    {"ticker": "USFR", "name": "WisdomTree Floating Rate Treasury", "type": "float", "stateExempt": True,
     "sec_yield": 4.28, "duration": 0.02, "expense": 0.15, "fallback_price": 50.43, "fallback_aum": "16.7B"},
    {"ticker": "TFLO", "name": "iShares Treasury Floating Rate Bond", "type": "float", "stateExempt": True,
     "sec_yield": 4.28, "duration": 0.01, "expense": 0.15, "fallback_price": 50.48, "fallback_aum": "6.5B"},
    {"ticker": "FLRN", "name": "SPDR Bloomberg IG Floating Rate ETF", "type": "float", "stateExempt": False,
     "sec_yield": 5.80, "duration": 0.01, "expense": 0.15, "fallback_price": 30.72, "fallback_aum": "2.7B"},
    {"ticker": "FLOT", "name": "iShares Floating Rate Bond ETF", "type": "corporate", "stateExempt": False,
     "sec_yield": 5.45, "duration": 0.01, "expense": 0.15, "fallback_price": 51.02, "fallback_aum": "9.0B"},
    # === CORPORATE / ULTRA-SHORT ===
    {"ticker": "JPST", "name": "JPMorgan Ultra-Short Income ETF", "type": "corporate", "stateExempt": False,
     "sec_yield": 4.92, "duration": 0.48, "expense": 0.18, "fallback_price": 50.71, "fallback_aum": "36.4B"},
    {"ticker": "MINT", "name": "PIMCO Enhanced Short Maturity Active", "type": "corporate", "stateExempt": False,
     "sec_yield": 4.98, "duration": 0.24, "expense": 0.36, "fallback_price": 100.56, "fallback_aum": "15.0B"},
    {"ticker": "ICSH", "name": "iShares Ultra Short-Term Bond ETF", "type": "corporate", "stateExempt": False,
     "sec_yield": 4.78, "duration": 0.38, "expense": 0.08, "fallback_price": 50.65, "fallback_aum": "6.6B"},
    {"ticker": "GSY", "name": "Invesco Ultra Short Duration ETF", "type": "corporate", "stateExempt": False,
     "sec_yield": 4.95, "duration": 0.35, "expense": 0.22, "fallback_price": 50.19, "fallback_aum": "3.2B"},
    {"ticker": "NEAR", "name": "iShares Short Duration Bond Active", "type": "corporate", "stateExempt": False,
     "sec_yield": 4.85, "duration": 0.52, "expense": 0.25, "fallback_price": 51.28, "fallback_aum": "3.8B"},
    {"ticker": "FTSM", "name": "First Trust Enhanced Short Maturity ETF", "type": "corporate", "stateExempt": False,
     "sec_yield": 5.02, "duration": 0.55, "expense": 0.45, "fallback_price": 60.05, "fallback_aum": "6.2B"},
    {"ticker": "VUSB", "name": "Vanguard Ultra-Short Bond ETF", "type": "corporate", "stateExempt": False,
     "sec_yield": 4.38, "duration": 0.50, "expense": 0.10, "fallback_price": 49.84, "fallback_aum": "7.7B"},
    # === CLO ===
    {"ticker": "JAAA", "name": "Janus Henderson AAA CLO ETF", "type": "clo", "stateExempt": False,
     "sec_yield": 5.20, "duration": 0.10, "expense": 0.21, "fallback_price": 50.73, "fallback_aum": "20.9B"},
    {"ticker": "CLOA", "name": "iShares AAA CLO Active ETF", "type": "clo", "stateExempt": False,
     "sec_yield": 5.60, "duration": 0.10, "expense": 0.20, "fallback_price": 51.82, "fallback_aum": "3.2B"},
    {"ticker": "JBBB", "name": "Janus Henderson B-BBB CLO ETF", "type": "clo", "stateExempt": False,
     "sec_yield": 6.20, "duration": 0.10, "expense": 0.49, "fallback_price": 47.78, "fallback_aum": "1.2B"},
    # === BOX SPREAD ===
    {"ticker": "BOXX", "name": "Alpha Architect 1-3 Month Box ETF", "type": "box", "stateExempt": False,
     "sec_yield": 4.18, "duration": 0.17, "expense": 0.19, "fallback_price": 115.68, "fallback_aum": "9.0B"},
]

# Non-ETF products that can't be fetched from Yahoo Finance
MANUAL_PRODUCTS = [
    {"ticker": "GFUND", "name": "TSP G Fund (Government Securities)", "type": "treasury", "stateExempt": True,
     "price": 19.50, "yield": 4.25, "duration": 0.00, "expense": 0.00, "aum": "230B",
     "url": "https://www.tsp.gov/funds-individual/g-fund/"},
]


def format_aum(market_cap):
    """Format AUM value to human readable string."""
    if market_cap is None or market_cap == 0:
        return "N/A"
    if market_cap >= 1e12:
        return f"{market_cap / 1e12:.1f}T"
    elif market_cap >= 1e9:
        return f"{market_cap / 1e9:.1f}B"
    elif market_cap >= 1e6:
        return f"{market_cap / 1e6:.0f}M"
    else:
        return f"{market_cap:.0f}"


def fetch_etf_data(ticker_symbol):
    """Fetch current price and AUM from Yahoo Finance."""
    try:
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info

        price = info.get("previousClose") or info.get("regularMarketPrice") or info.get("navPrice")

        # For ETFs, totalAssets is typically the AUM
        aum = info.get("totalAssets") or info.get("marketCap")

        return {
            "price": round(price, 2) if price else None,
            "aum": format_aum(aum) if aum else None,
        }
    except Exception as e:
        print(f"  Warning: Failed to fetch {ticker_symbol}: {e}")
        return {"price": None, "aum": None}


def main():
    print(f"=== Fixed Income Dashboard Data Update ===")
    print(f"Time: {datetime.now(timezone.utc).isoformat()}")
    print()

    products = []
    errors = []

    # Fetch ETF data from Yahoo Finance
    tickers = [p["ticker"] for p in PRODUCTS]
    print(f"Fetching data for {len(tickers)} ETFs...")

    for config in PRODUCTS:
        ticker = config["ticker"]
        print(f"  Fetching {ticker}...", end=" ")

        live = fetch_etf_data(ticker)

        if live["price"] is None:
            errors.append(f"{ticker}: Could not fetch price, using fallback")
            print("FAILED (using fallback)")
            # Use fallback price from config if available
            fallback_price = config.get("fallback_price")
            fallback_aum = config.get("fallback_aum", "N/A")
            if fallback_price is None:
                continue
            live = {"price": fallback_price, "aum": fallback_aum}

        product = {
            "ticker": ticker,
            "name": config["name"],
            "type": config["type"],
            "stateExempt": config["stateExempt"],
            "price": live["price"],
            "yield": config["sec_yield"],
            "duration": config["duration"],
            "expense": config["expense"],
            "aum": live["aum"] or "N/A",
        }

        products.append(product)
        print(f"${live['price']} | AUM: {live['aum'] or 'N/A'}")

    # Add manual products (GFUND, etc.)
    for manual in MANUAL_PRODUCTS:
        print(f"  Adding {manual['ticker']} (manual)...", end=" ")
        products.append(manual)
        print("OK")

    print(f"\nTotal products: {len(products)}")
    if errors:
        print(f"Errors ({len(errors)}):")
        for e in errors:
            print(f"  - {e}")

    # Build output JSON
    output = {
        "lastUpdated": datetime.now(timezone.utc).isoformat(),
        "products": products
    }

    # Write to data file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_dir = os.path.dirname(script_dir)
    data_path = os.path.join(repo_dir, "data", "etf_data.json")

    os.makedirs(os.path.dirname(data_path), exist_ok=True)

    with open(data_path, "w") as f:
        json.dump(output, f, indent=2)

    print(f"\nData written to {data_path}")
    print(f"Products: {len(products)}, Updated: {output['lastUpdated']}")

    return 0 if len(products) > 0 else 1


if __name__ == "__main__":
    sys.exit(main())

