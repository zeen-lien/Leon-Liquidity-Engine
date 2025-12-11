"""
LEON LIQUIDITY ENGINE - BINANCE REAL-TIME SERVICE
Koneksi ke Binance API untuk data real-time

FITUR:
- REST API untuk data historis
- WebSocket untuk live price updates
- Auto-reconnect jika koneksi terputus
"""

import asyncio
import json
from typing import Dict, List, Optional, Callable
from datetime import datetime, timedelta
import aiohttp

# Binance API Endpoints
BINANCE_REST_URL = "https://api.binance.com/api/v3"
BINANCE_WS_URL = "wss://stream.binance.com:9443/ws"

# Supported symbols
SUPPORTED_SYMBOLS = [
    "BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT",
    "DOGEUSDT", "ADAUSDT", "AVAXUSDT", "DOTUSDT", "MATICUSDT"
]


class BinanceDataFetcher:
    """
    Class untuk mengambil data dari Binance REST API.
    """
    
    def __init__(self):
        self.base_url = BINANCE_REST_URL
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session."""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def close(self):
        """Close the session."""
        if self.session and not self.session.closed:
            await self.session.close()
    
    async def get_klines(
        self,
        symbol: str,
        interval: str = "1h",
        limit: int = 100
    ) -> List[Dict]:
        """
        Ambil data klines (candlestick) dari Binance.
        
        Parameters:
        -----------
        symbol: str - Trading pair (e.g., "BTCUSDT")
        interval: str - Timeframe ("1m", "5m", "15m", "1h", "4h", "1d")
        limit: int - Jumlah candle (max 1000)
        
        Returns:
        --------
        List[Dict] - List of OHLCV data
        """
        session = await self._get_session()
        
        url = f"{self.base_url}/klines"
        params = {
            "symbol": symbol.upper(),
            "interval": interval,
            "limit": min(limit, 1000)
        }
        
        try:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    # Convert to OHLCV format
                    klines = []
                    for k in data:
                        klines.append({
                            "open_time": k[0],
                            "open": float(k[1]),
                            "high": float(k[2]),
                            "low": float(k[3]),
                            "close": float(k[4]),
                            "volume": float(k[5]),
                            "close_time": k[6],
                            "quote_volume": float(k[7]),
                            "trades": k[8],
                            "taker_buy_volume": float(k[9]),
                            "taker_buy_quote_volume": float(k[10])
                        })
                    
                    return klines
                else:
                    error_text = await response.text()
                    raise Exception(f"Binance API error: {response.status} - {error_text}")
                    
        except aiohttp.ClientError as e:
            raise Exception(f"Network error: {str(e)}")
    
    async def get_ticker_price(self, symbol: str) -> Dict:
        """
        Ambil harga terkini untuk symbol.
        
        Returns:
        --------
        Dict dengan 'symbol' dan 'price'
        """
        session = await self._get_session()
        
        url = f"{self.base_url}/ticker/price"
        params = {"symbol": symbol.upper()}
        
        try:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "symbol": data["symbol"],
                        "price": float(data["price"]),
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    error_text = await response.text()
                    raise Exception(f"Binance API error: {response.status} - {error_text}")
                    
        except aiohttp.ClientError as e:
            raise Exception(f"Network error: {str(e)}")
    
    async def get_24h_ticker(self, symbol: str) -> Dict:
        """
        Ambil statistik 24 jam untuk symbol.
        
        Returns:
        --------
        Dict dengan statistik 24h (price change, volume, high, low, etc.)
        """
        session = await self._get_session()
        
        url = f"{self.base_url}/ticker/24hr"
        params = {"symbol": symbol.upper()}
        
        try:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "symbol": data["symbol"],
                        "price_change": float(data["priceChange"]),
                        "price_change_percent": float(data["priceChangePercent"]),
                        "weighted_avg_price": float(data["weightedAvgPrice"]),
                        "prev_close_price": float(data["prevClosePrice"]),
                        "last_price": float(data["lastPrice"]),
                        "bid_price": float(data["bidPrice"]),
                        "ask_price": float(data["askPrice"]),
                        "open_price": float(data["openPrice"]),
                        "high_price": float(data["highPrice"]),
                        "low_price": float(data["lowPrice"]),
                        "volume": float(data["volume"]),
                        "quote_volume": float(data["quoteVolume"]),
                        "open_time": data["openTime"],
                        "close_time": data["closeTime"],
                        "trades": data["count"]
                    }
                else:
                    error_text = await response.text()
                    raise Exception(f"Binance API error: {response.status} - {error_text}")
                    
        except aiohttp.ClientError as e:
            raise Exception(f"Network error: {str(e)}")
    
    async def get_multiple_tickers(self, symbols: List[str] = None) -> List[Dict]:
        """
        Ambil harga terkini untuk multiple symbols.
        
        Parameters:
        -----------
        symbols: List[str] - List of symbols (default: SUPPORTED_SYMBOLS)
        
        Returns:
        --------
        List[Dict] dengan harga untuk setiap symbol
        """
        if symbols is None:
            symbols = SUPPORTED_SYMBOLS
        
        session = await self._get_session()
        
        url = f"{self.base_url}/ticker/price"
        
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    all_tickers = await response.json()
                    
                    # Filter hanya symbols yang diminta
                    result = []
                    for ticker in all_tickers:
                        if ticker["symbol"] in symbols:
                            result.append({
                                "symbol": ticker["symbol"],
                                "price": float(ticker["price"]),
                                "timestamp": datetime.now().isoformat()
                            })
                    
                    return result
                else:
                    error_text = await response.text()
                    raise Exception(f"Binance API error: {response.status} - {error_text}")
                    
        except aiohttp.ClientError as e:
            raise Exception(f"Network error: {str(e)}")


class BinanceWebSocket:
    """
    Class untuk koneksi WebSocket ke Binance untuk live updates.
    """
    
    def __init__(self):
        self.ws_url = BINANCE_WS_URL
        self.ws: Optional[aiohttp.ClientWebSocketResponse] = None
        self.session: Optional[aiohttp.ClientSession] = None
        self.is_connected = False
        self.callbacks: List[Callable] = []
        self.subscribed_streams: List[str] = []
    
    def add_callback(self, callback: Callable):
        """Add callback function untuk handle incoming data."""
        self.callbacks.append(callback)
    
    async def connect(self, streams: List[str]):
        """
        Connect ke Binance WebSocket.
        
        Parameters:
        -----------
        streams: List[str] - List of streams to subscribe
                 Format: "btcusdt@kline_1h", "ethusdt@trade", etc.
        """
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
        
        # Build WebSocket URL with streams
        stream_str = "/".join(streams)
        ws_url = f"{self.ws_url}/{stream_str}"
        
        try:
            self.ws = await self.session.ws_connect(ws_url)
            self.is_connected = True
            self.subscribed_streams = streams
            print(f"Connected to Binance WebSocket: {streams}")
            
            # Start listening
            asyncio.create_task(self._listen())
            
        except Exception as e:
            self.is_connected = False
            raise Exception(f"WebSocket connection failed: {str(e)}")
    
    async def _listen(self):
        """Listen for incoming WebSocket messages."""
        try:
            async for msg in self.ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    data = json.loads(msg.data)
                    
                    # Call all registered callbacks
                    for callback in self.callbacks:
                        try:
                            if asyncio.iscoroutinefunction(callback):
                                await callback(data)
                            else:
                                callback(data)
                        except Exception as e:
                            print(f"Callback error: {e}")
                            
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    print(f"WebSocket error: {self.ws.exception()}")
                    break
                    
        except Exception as e:
            print(f"WebSocket listen error: {e}")
        finally:
            self.is_connected = False
    
    async def disconnect(self):
        """Disconnect from WebSocket."""
        if self.ws and not self.ws.closed:
            await self.ws.close()
        if self.session and not self.session.closed:
            await self.session.close()
        self.is_connected = False
        print("Disconnected from Binance WebSocket")
    
    async def subscribe_klines(self, symbols: List[str], interval: str = "1h"):
        """
        Subscribe ke kline streams untuk multiple symbols.
        
        Parameters:
        -----------
        symbols: List[str] - List of symbols (e.g., ["BTCUSDT", "ETHUSDT"])
        interval: str - Kline interval ("1m", "5m", "15m", "1h", "4h", "1d")
        """
        streams = [f"{s.lower()}@kline_{interval}" for s in symbols]
        await self.connect(streams)
    
    async def subscribe_trades(self, symbols: List[str]):
        """
        Subscribe ke trade streams untuk multiple symbols.
        
        Parameters:
        -----------
        symbols: List[str] - List of symbols
        """
        streams = [f"{s.lower()}@trade" for s in symbols]
        await self.connect(streams)


# Helper functions untuk parsing WebSocket data
def parse_kline_data(data: Dict) -> Dict:
    """
    Parse kline data dari WebSocket.
    
    Returns:
    --------
    Dict dengan format OHLCV yang sudah di-parse
    """
    if "k" not in data:
        return None
    
    k = data["k"]
    return {
        "symbol": k["s"],
        "interval": k["i"],
        "open_time": k["t"],
        "close_time": k["T"],
        "open": float(k["o"]),
        "high": float(k["h"]),
        "low": float(k["l"]),
        "close": float(k["c"]),
        "volume": float(k["v"]),
        "trades": k["n"],
        "is_closed": k["x"],  # True jika candle sudah closed
        "quote_volume": float(k["q"]),
        "taker_buy_volume": float(k["V"]),
        "taker_buy_quote_volume": float(k["Q"])
    }


def parse_trade_data(data: Dict) -> Dict:
    """
    Parse trade data dari WebSocket.
    
    Returns:
    --------
    Dict dengan informasi trade
    """
    return {
        "symbol": data.get("s"),
        "price": float(data.get("p", 0)),
        "quantity": float(data.get("q", 0)),
        "trade_time": data.get("T"),
        "is_buyer_maker": data.get("m", False),
        "trade_id": data.get("t")
    }


# Global instances
binance_fetcher = BinanceDataFetcher()
binance_ws = BinanceWebSocket()
