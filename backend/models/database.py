"""
Database models untuk Leon Liquidity Engine.
Menggunakan SQLAlchemy untuk ORM.
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import enum

from ..core.config import DATABASE_URL

# Setup database
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class MarketType(enum.Enum):
    """Tipe market: SPOT atau FUTURES"""
    SPOT = "SPOT"
    FUTURES = "FUTURES"


class SignalType(enum.Enum):
    """Tipe sinyal: BELI atau JUAL"""
    BELI = "BELI"
    JUAL = "JUAL"


class SignalStatus(enum.Enum):
    """Status sinyal"""
    OPEN = "OPEN"           # Sinyal masih aktif
    HIT_TP = "HIT_TP"       # Kena Take Profit
    HIT_SL = "HIT_SL"       # Kena Stop Loss
    EXPIRED = "EXPIRED"     # Expired tanpa kena SL/TP
    CANCELLED = "CANCELLED" # Dibatalkan manual


class FavoritePair(Base):
    """Model untuk menyimpan pair favorit user"""
    __tablename__ = "favorite_pairs"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), unique=True, index=True, nullable=False)
    market_type = Column(SQLEnum(MarketType), default=MarketType.FUTURES)
    added_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    def __repr__(self):
        return f"<FavoritePair {self.symbol} ({self.market_type.value})>"


class Signal(Base):
    """Model untuk menyimpan history sinyal trading"""
    __tablename__ = "signals"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Identifikasi
    symbol = Column(String(20), index=True, nullable=False)
    market_type = Column(SQLEnum(MarketType), default=MarketType.FUTURES)
    
    # Sinyal
    signal_type = Column(SQLEnum(SignalType), nullable=False)
    entry_price = Column(Float, nullable=False)
    stop_loss = Column(Float, nullable=False)
    take_profit = Column(Float, nullable=False)
    
    # Confidence & Analysis
    confidence = Column(Float, nullable=False)
    confluence_status = Column(String(20))  # STRONG, WEAK, LSTM_ONLY
    technical_confidence = Column(Float)
    lstm_confidence = Column(Float)
    lstm_direction = Column(String(10))
    alasan = Column(String(500))
    
    # Trading Mode
    mode_trading = Column(String(20), default="santai")
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    closed_at = Column(DateTime, nullable=True)
    
    # Status & Result
    status = Column(SQLEnum(SignalStatus), default=SignalStatus.OPEN, index=True)
    exit_price = Column(Float, nullable=True)
    pnl_percent = Column(Float, nullable=True)
    pnl_usdt = Column(Float, nullable=True)
    duration_minutes = Column(Integer, nullable=True)
    
    # Price tracking
    highest_price = Column(Float, nullable=True)  # Highest price sejak entry
    lowest_price = Column(Float, nullable=True)   # Lowest price sejak entry
    
    def __repr__(self):
        return f"<Signal {self.symbol} {self.signal_type.value} @ {self.entry_price}>"
    
    def calculate_pnl(self, exit_price: float) -> float:
        """Hitung PnL dalam persen"""
        if self.signal_type == SignalType.BELI:
            return ((exit_price - self.entry_price) / self.entry_price) * 100
        else:
            return ((self.entry_price - exit_price) / self.entry_price) * 100


class SignalStatistics(Base):
    """Model untuk menyimpan statistik harian"""
    __tablename__ = "signal_statistics"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, index=True, nullable=False)
    
    # Counts
    total_signals = Column(Integer, default=0)
    total_beli = Column(Integer, default=0)
    total_jual = Column(Integer, default=0)
    hit_tp = Column(Integer, default=0)
    hit_sl = Column(Integer, default=0)
    expired = Column(Integer, default=0)
    
    # Performance
    win_rate = Column(Float, default=0.0)
    avg_pnl = Column(Float, default=0.0)
    total_pnl = Column(Float, default=0.0)
    best_trade_pnl = Column(Float, default=0.0)
    worst_trade_pnl = Column(Float, default=0.0)
    
    # By Market
    spot_signals = Column(Integer, default=0)
    futures_signals = Column(Integer, default=0)
    
    def __repr__(self):
        return f"<Statistics {self.date.strftime('%Y-%m-%d')} WR:{self.win_rate}%>"


# Create all tables
def init_db():
    """Initialize database dan create tables"""
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")


def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
