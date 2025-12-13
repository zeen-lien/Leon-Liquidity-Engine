"""
Helper functions untuk Leon Liquidity Engine.
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
import math


def format_price(price: float, decimals: int = 2) -> str:
    """Format harga dengan decimal yang sesuai"""
    if price >= 1:
        return f"{price:,.{decimals}f}"
    elif price >= 0.0001:
        return f"{price:.6f}"
    else:
        return f"{price:.8f}"


def format_percent(value: float, include_sign: bool = True) -> str:
    """Format persentase"""
    sign = "+" if value > 0 and include_sign else ""
    return f"{sign}{value:.2f}%"


def format_timestamp(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Format datetime ke string"""
    return dt.strftime(format_str)


def calculate_pnl_percent(entry: float, exit: float, is_long: bool = True) -> float:
    """Hitung PnL dalam persen"""
    if is_long:
        return ((exit - entry) / entry) * 100
    else:
        return ((entry - exit) / entry) * 100


def calculate_risk_reward(entry: float, sl: float, tp: float, is_long: bool = True) -> float:
    """Hitung risk reward ratio"""
    if is_long:
        risk = entry - sl
        reward = tp - entry
    else:
        risk = sl - entry
        reward = entry - tp
    
    if risk <= 0:
        return 0
    return reward / risk


def get_price_decimals(price: float) -> int:
    """Tentukan jumlah decimal berdasarkan harga"""
    if price >= 1000:
        return 2
    elif price >= 1:
        return 4
    elif price >= 0.01:
        return 6
    else:
        return 8


def round_to_tick(price: float, tick_size: float = 0.01) -> float:
    """Round harga ke tick size terdekat"""
    return round(price / tick_size) * tick_size


def calculate_position_size(
    account_balance: float,
    risk_percent: float,
    entry_price: float,
    stop_loss: float
) -> float:
    """Hitung position size berdasarkan risk management"""
    risk_amount = account_balance * (risk_percent / 100)
    price_diff = abs(entry_price - stop_loss)
    
    if price_diff == 0:
        return 0
    
    position_size = risk_amount / price_diff
    return position_size


def time_ago(dt: datetime) -> str:
    """Convert datetime ke format 'X waktu yang lalu'"""
    now = datetime.utcnow()
    diff = now - dt
    
    seconds = diff.total_seconds()
    
    if seconds < 60:
        return f"{int(seconds)} detik lalu"
    elif seconds < 3600:
        minutes = int(seconds / 60)
        return f"{minutes} menit lalu"
    elif seconds < 86400:
        hours = int(seconds / 3600)
        return f"{hours} jam lalu"
    else:
        days = int(seconds / 86400)
        return f"{days} hari lalu"


def get_crypto_color(symbol: str) -> str:
    """Get warna untuk cryptocurrency"""
    colors = {
        "BTC": "#ff9500",
        "ETH": "#00d4ff",
        "BNB": "#f0b90b",
        "SOL": "#14f195",
        "XRP": "#00aae4",
        "DOGE": "#ffcc00",
        "ADA": "#ff1493",
        "AVAX": "#e84142",
        "DOT": "#e6007a",
        "MATIC": "#8247e5",
        "LINK": "#2a5ada",
        "LTC": "#bfbbbb",
        "ATOM": "#2e3148",
        "UNI": "#ff007a",
        "APT": "#00d4aa",
        "PEPE": "#39ff14",
        "MANTA": "#00fff7",
        "SUI": "#4da2ff",
        "SEI": "#9b1c1c",
        "TIA": "#7b3fe4",
    }
    
    # Extract base symbol (remove USDT)
    base = symbol.replace("USDT", "").replace("BUSD", "").replace("PERP", "")
    return colors.get(base, "#ffffff")


def validate_symbol(symbol: str) -> bool:
    """Validasi format symbol"""
    if not symbol:
        return False
    
    # Harus uppercase
    if symbol != symbol.upper():
        return False
    
    # Harus diakhiri dengan USDT atau BUSD
    if not (symbol.endswith("USDT") or symbol.endswith("BUSD")):
        return False
    
    # Minimal 5 karakter (misal: BTCUSDT)
    if len(symbol) < 5:
        return False
    
    return True


def parse_interval(interval: str) -> int:
    """Parse interval string ke menit"""
    intervals = {
        "1m": 1,
        "3m": 3,
        "5m": 5,
        "15m": 15,
        "30m": 30,
        "1h": 60,
        "2h": 120,
        "4h": 240,
        "6h": 360,
        "8h": 480,
        "12h": 720,
        "1d": 1440,
        "3d": 4320,
        "1w": 10080,
    }
    return intervals.get(interval, 60)
