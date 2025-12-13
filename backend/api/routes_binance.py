"""
API Routes untuk Binance Integration.
Support untuk SPOT dan FUTURES market.
"""

from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
import aiohttp
from datetime import datetime

from ..core.config import (
    BINANCE_SPOT_BASE_URL,
    BINANCE_FUTURES_BASE_URL,
    DEFAULT_SPOT_SYMBOLS,
    DEFAULT_FUTURES_SYMBOLS,
)

router = APIRouter(prefix="/binance", tags=["Binance"])


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

async def fetch_binance(url: str, params: dict = None) -> dict:
    """Fetch data dari Binance API"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status != 200:
                raise HTTPException(
                    status_code=response.status,
                    detail=f"Binance API error: {await response.text()}"
                )
            return await response.json()


# ============================================================================
# SPOT ENDPOINTS
# ============================================================================

@router.get("/spot/price/{symbol}")
async def get_spot_price(symbol: str):
    """Ambil harga spot untuk symbol tertentu"""
    url = f"{BINANCE_SPOT_BASE_URL}/api/v3/ticker/price"
    data = await fetch_binance(url, {"symbol": symbol.upper()})
    
    return {
        "status": "sukses",
        "market": "SPOT",
        "symbol": data["symbol"],
        "price": float(data["price"]),
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/spot/prices")
async def get_spot_prices(symbols: Optional[str] = None):
    """Ambil harga spot untuk multiple symbols"""
    url = f"{BINANCE_SPOT_BASE_URL}/api/v3/ticker/price"
    
    if symbols:
        symbol_list = [s.strip().upper() for s in symbols.split(",")]
    else:
        symbol_list = DEFAULT_SPOT_SYMBOLS
    
    all_prices = await fetch_binance(url)
    
    filtered = [
        {
            "symbol": p["symbol"],
            "price": float(p["price"]),
            "timestamp": datetime.utcnow().isoformat()
        }
        for p in all_prices
        if p["symbol"] in symbol_list
    ]
    
    return {
        "status": "sukses",
        "market": "SPOT",
        "jumlah": len(filtered),
        "data": filtered
    }


@router.get("/spot/ticker24h/{symbol}")
async def get_spot_ticker_24h(symbol: str):
    """Ambil statistik 24h untuk spot"""
    url = f"{BINANCE_SPOT_BASE_URL}/api/v3/ticker/24hr"
    data = await fetch_binance(url, {"symbol": symbol.upper()})
    
    return {
        "status": "sukses",
        "market": "SPOT",
        "symbol": data["symbol"],
        "price": float(data["lastPrice"]),
        "change_24h": float(data["priceChangePercent"]),
        "high_24h": float(data["highPrice"]),
        "low_24h": float(data["lowPrice"]),
        "volume_24h": float(data["volume"]),
        "quote_volume_24h": float(data["quoteVolume"]),
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/spot/klines/{symbol}")
async def get_spot_klines(
    symbol: str,
    interval: str = Query("1h", description="1m,5m,15m,1h,4h,1d"),
    limit: int = Query(100, ge=1, le=1000)
):
    """Ambil candlestick data untuk spot"""
    url = f"{BINANCE_SPOT_BASE_URL}/api/v3/klines"
    data = await fetch_binance(url, {
        "symbol": symbol.upper(),
        "interval": interval,
        "limit": limit
    })
    
    klines = [
        {
            "open_time": k[0],
            "open": float(k[1]),
            "high": float(k[2]),
            "low": float(k[3]),
            "close": float(k[4]),
            "volume": float(k[5]),
            "close_time": k[6],
            "quote_volume": float(k[7]),
            "trades": k[8],
        }
        for k in data
    ]
    
    return {
        "status": "sukses",
        "market": "SPOT",
        "symbol": symbol.upper(),
        "interval": interval,
        "jumlah": len(klines),
        "data": klines
    }


# ============================================================================
# FUTURES ENDPOINTS
# ============================================================================

@router.get("/futures/price/{symbol}")
async def get_futures_price(symbol: str):
    """Ambil harga futures untuk symbol tertentu"""
    url = f"{BINANCE_FUTURES_BASE_URL}/fapi/v1/ticker/price"
    data = await fetch_binance(url, {"symbol": symbol.upper()})
    
    return {
        "status": "sukses",
        "market": "FUTURES",
        "symbol": data["symbol"],
        "price": float(data["price"]),
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/futures/prices")
async def get_futures_prices(symbols: Optional[str] = None):
    """Ambil harga futures untuk multiple symbols"""
    url = f"{BINANCE_FUTURES_BASE_URL}/fapi/v1/ticker/price"
    
    if symbols:
        symbol_list = [s.strip().upper() for s in symbols.split(",")]
    else:
        symbol_list = DEFAULT_FUTURES_SYMBOLS
    
    all_prices = await fetch_binance(url)
    
    filtered = [
        {
            "symbol": p["symbol"],
            "price": float(p["price"]),
            "timestamp": datetime.utcnow().isoformat()
        }
        for p in all_prices
        if p["symbol"] in symbol_list
    ]
    
    return {
        "status": "sukses",
        "market": "FUTURES",
        "jumlah": len(filtered),
        "data": filtered
    }


@router.get("/futures/ticker24h/{symbol}")
async def get_futures_ticker_24h(symbol: str):
    """Ambil statistik 24h untuk futures"""
    url = f"{BINANCE_FUTURES_BASE_URL}/fapi/v1/ticker/24hr"
    data = await fetch_binance(url, {"symbol": symbol.upper()})
    
    return {
        "status": "sukses",
        "market": "FUTURES",
        "symbol": data["symbol"],
        "price": float(data["lastPrice"]),
        "change_24h": float(data["priceChangePercent"]),
        "high_24h": float(data["highPrice"]),
        "low_24h": float(data["lowPrice"]),
        "volume_24h": float(data["volume"]),
        "quote_volume_24h": float(data["quoteVolume"]),
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/futures/klines/{symbol}")
async def get_futures_klines(
    symbol: str,
    interval: str = Query("1h", description="1m,5m,15m,1h,4h,1d"),
    limit: int = Query(100, ge=1, le=1000)
):
    """Ambil candlestick data untuk futures"""
    url = f"{BINANCE_FUTURES_BASE_URL}/fapi/v1/klines"
    data = await fetch_binance(url, {
        "symbol": symbol.upper(),
        "interval": interval,
        "limit": limit
    })
    
    klines = [
        {
            "open_time": k[0],
            "open": float(k[1]),
            "high": float(k[2]),
            "low": float(k[3]),
            "close": float(k[4]),
            "volume": float(k[5]),
            "close_time": k[6],
            "quote_volume": float(k[7]),
            "trades": k[8],
        }
        for k in data
    ]
    
    return {
        "status": "sukses",
        "market": "FUTURES",
        "symbol": symbol.upper(),
        "interval": interval,
        "jumlah": len(klines),
        "data": klines
    }


@router.get("/futures/funding/{symbol}")
async def get_funding_rate(symbol: str):
    """Ambil funding rate untuk futures"""
    url = f"{BINANCE_FUTURES_BASE_URL}/fapi/v1/fundingRate"
    data = await fetch_binance(url, {"symbol": symbol.upper(), "limit": 1})
    
    if not data:
        raise HTTPException(status_code=404, detail="Funding rate tidak ditemukan")
    
    latest = data[0]
    
    return {
        "status": "sukses",
        "symbol": latest["symbol"],
        "funding_rate": float(latest["fundingRate"]),
        "funding_rate_percent": float(latest["fundingRate"]) * 100,
        "funding_time": latest["fundingTime"],
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/futures/open-interest/{symbol}")
async def get_open_interest(symbol: str):
    """Ambil open interest untuk futures"""
    url = f"{BINANCE_FUTURES_BASE_URL}/fapi/v1/openInterest"
    data = await fetch_binance(url, {"symbol": symbol.upper()})
    
    return {
        "status": "sukses",
        "symbol": data["symbol"],
        "open_interest": float(data["openInterest"]),
        "timestamp": datetime.utcnow().isoformat()
    }


# ============================================================================
# SEARCH & DISCOVERY
# ============================================================================

@router.get("/search")
async def search_symbols(
    query: str = Query(..., min_length=2, description="Search query"),
    market: str = Query("FUTURES", description="SPOT atau FUTURES")
):
    """Search symbols berdasarkan query"""
    if market.upper() == "SPOT":
        url = f"{BINANCE_SPOT_BASE_URL}/api/v3/exchangeInfo"
    else:
        url = f"{BINANCE_FUTURES_BASE_URL}/fapi/v1/exchangeInfo"
    
    data = await fetch_binance(url)
    
    query_upper = query.upper()
    matches = [
        {
            "symbol": s["symbol"],
            "base": s["baseAsset"],
            "quote": s["quoteAsset"],
            "status": s["status"]
        }
        for s in data["symbols"]
        if query_upper in s["symbol"] and s["quoteAsset"] == "USDT" and s["status"] == "TRADING"
    ][:20]  # Limit 20 results
    
    return {
        "status": "sukses",
        "market": market.upper(),
        "query": query,
        "jumlah": len(matches),
        "results": matches
    }


@router.get("/all-symbols")
async def get_all_symbols(market: str = Query("FUTURES", description="SPOT atau FUTURES")):
    """Ambil semua symbols yang tersedia"""
    if market.upper() == "SPOT":
        url = f"{BINANCE_SPOT_BASE_URL}/api/v3/exchangeInfo"
    else:
        url = f"{BINANCE_FUTURES_BASE_URL}/fapi/v1/exchangeInfo"
    
    data = await fetch_binance(url)
    
    symbols = [
        {
            "symbol": s["symbol"],
            "base": s["baseAsset"],
            "quote": s["quoteAsset"],
        }
        for s in data["symbols"]
        if s["quoteAsset"] == "USDT" and s["status"] == "TRADING"
    ]
    
    return {
        "status": "sukses",
        "market": market.upper(),
        "jumlah": len(symbols),
        "symbols": symbols
    }
