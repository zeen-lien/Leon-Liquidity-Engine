"""
Konfigurasi aplikasi Leon Liquidity Engine.
Semua settings dan constants ada di sini.
"""

from pathlib import Path
from typing import List

# ============================================================================
# PATH CONFIGURATION
# ============================================================================
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
UPLOADS_DIR = DATA_DIR / "uploads"
PROCESSED_DIR = DATA_DIR / "processed"
MODELS_DIR = DATA_DIR / "models"
DATABASE_DIR = DATA_DIR / "database"

# Pastikan folder ada
for folder in [UPLOADS_DIR, PROCESSED_DIR, MODELS_DIR, DATABASE_DIR]:
    folder.mkdir(parents=True, exist_ok=True)

# ============================================================================
# DATABASE CONFIGURATION
# ============================================================================
DATABASE_URL = f"sqlite:///{DATABASE_DIR}/leon_engine.db"

# ============================================================================
# BINANCE API CONFIGURATION
# ============================================================================
BINANCE_SPOT_BASE_URL = "https://api.binance.com"
BINANCE_FUTURES_BASE_URL = "https://fapi.binance.com"
BINANCE_SPOT_WS_URL = "wss://stream.binance.com:9443"
BINANCE_FUTURES_WS_URL = "wss://fstream.binance.com"

# Default symbols untuk monitoring
DEFAULT_SPOT_SYMBOLS: List[str] = [
    "BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT",
    "DOGEUSDT", "ADAUSDT", "AVAXUSDT", "DOTUSDT", "MATICUSDT"
]

DEFAULT_FUTURES_SYMBOLS: List[str] = [
    "BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT",
    "DOGEUSDT", "ADAUSDT", "AVAXUSDT", "DOTUSDT", "MATICUSDT",
    "LINKUSDT", "LTCUSDT", "ATOMUSDT", "UNIUSDT", "APTUSDT"
]

# ============================================================================
# TRADING CONFIGURATION
# ============================================================================
TRADING_MODES = {
    "aktif": {
        "nama": "Aktif",
        "deskripsi": "Trading aktif dengan holding 1-4 jam",
        "rsi_period": 6,
        "rsi_oversold": 25,
        "rsi_overbought": 75,
        "risk_reward": 2.0,
        "max_holding_hours": 4
    },
    "santai": {
        "nama": "Santai",
        "deskripsi": "Trading santai dengan holding 4-12 jam",
        "rsi_period": 8,
        "rsi_oversold": 30,
        "rsi_overbought": 70,
        "risk_reward": 2.5,
        "max_holding_hours": 12
    },
    "pasif": {
        "nama": "Pasif",
        "deskripsi": "Trading pasif dengan holding 12-24 jam",
        "rsi_period": 14,
        "rsi_oversold": 35,
        "rsi_overbought": 65,
        "risk_reward": 3.0,
        "max_holding_hours": 24
    }
}

# ============================================================================
# SIGNAL CONFIGURATION
# ============================================================================
MIN_CONFIDENCE = 0.60  # Minimum confidence untuk generate sinyal
AUTO_SIGNAL_INTERVAL = 300  # Interval auto signal dalam detik (5 menit)

# ============================================================================
# LSTM MODEL CONFIGURATION
# ============================================================================
LSTM_SEQUENCE_LENGTH = 60  # Jumlah candle untuk input LSTM
LSTM_FEATURES = ["close", "volume", "rsi_14", "ema_20", "ema_50", "atr_14"]
LSTM_EPOCHS = 50
LSTM_BATCH_SIZE = 32
