"""
API Routes untuk Signal Management.
Endpoint untuk generate, track, dan manage trading signals.
"""

from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from ..models import (
    get_db, Signal, SignalStatus, SignalType, MarketType,
    FavoritePair, SignalStatistics
)

router = APIRouter(prefix="/signals", tags=["Signals"])


# ============================================================================
# PYDANTIC SCHEMAS
# ============================================================================

class SignalCreate(BaseModel):
    """Schema untuk membuat sinyal baru"""
    symbol: str = Field(..., description="Trading pair (e.g., BTCUSDT)")
    market_type: str = Field("FUTURES", description="SPOT atau FUTURES")
    signal_type: str = Field(..., description="BELI atau JUAL")
    entry_price: float = Field(..., gt=0)
    stop_loss: float = Field(..., gt=0)
    take_profit: float = Field(..., gt=0)
    confidence: float = Field(..., ge=0, le=1)
    mode_trading: str = Field("santai")
    alasan: Optional[str] = None
    confluence_status: Optional[str] = None
    technical_confidence: Optional[float] = None
    lstm_confidence: Optional[float] = None
    lstm_direction: Optional[str] = None


class SignalResponse(BaseModel):
    """Schema response untuk sinyal"""
    id: int
    symbol: str
    market_type: str
    signal_type: str
    entry_price: float
    stop_loss: float
    take_profit: float
    confidence: float
    status: str
    created_at: datetime
    closed_at: Optional[datetime]
    pnl_percent: Optional[float]
    alasan: Optional[str]
    
    class Config:
        from_attributes = True


class FavoriteCreate(BaseModel):
    """Schema untuk menambah pair favorit"""
    symbol: str = Field(..., min_length=5, max_length=20)
    market_type: str = Field("FUTURES")


# ============================================================================
# SIGNAL ENDPOINTS
# ============================================================================

@router.post("/create", response_model=SignalResponse)
async def create_signal(signal: SignalCreate, db: Session = Depends(get_db)):
    """
    Buat sinyal trading baru.
    Sinyal akan otomatis di-track untuk SL/TP.
    """
    # Cek apakah ada sinyal OPEN untuk symbol yang sama
    existing = db.query(Signal).filter(
        Signal.symbol == signal.symbol.upper(),
        Signal.status == SignalStatus.OPEN
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Sudah ada sinyal OPEN untuk {signal.symbol}. Tunggu sampai kena SL/TP."
        )
    
    # Buat sinyal baru
    new_signal = Signal(
        symbol=signal.symbol.upper(),
        market_type=MarketType[signal.market_type],
        signal_type=SignalType[signal.signal_type],
        entry_price=signal.entry_price,
        stop_loss=signal.stop_loss,
        take_profit=signal.take_profit,
        confidence=signal.confidence,
        mode_trading=signal.mode_trading,
        alasan=signal.alasan,
        confluence_status=signal.confluence_status,
        technical_confidence=signal.technical_confidence,
        lstm_confidence=signal.lstm_confidence,
        lstm_direction=signal.lstm_direction,
        highest_price=signal.entry_price,
        lowest_price=signal.entry_price,
    )
    
    db.add(new_signal)
    db.commit()
    db.refresh(new_signal)
    
    return SignalResponse(
        id=new_signal.id,
        symbol=new_signal.symbol,
        market_type=new_signal.market_type.value,
        signal_type=new_signal.signal_type.value,
        entry_price=new_signal.entry_price,
        stop_loss=new_signal.stop_loss,
        take_profit=new_signal.take_profit,
        confidence=new_signal.confidence,
        status=new_signal.status.value,
        created_at=new_signal.created_at,
        closed_at=new_signal.closed_at,
        pnl_percent=new_signal.pnl_percent,
        alasan=new_signal.alasan,
    )


@router.get("/active", response_model=List[SignalResponse])
async def get_active_signals(db: Session = Depends(get_db)):
    """Ambil semua sinyal yang masih OPEN"""
    signals = db.query(Signal).filter(
        Signal.status == SignalStatus.OPEN
    ).order_by(Signal.created_at.desc()).all()
    
    return [
        SignalResponse(
            id=s.id,
            symbol=s.symbol,
            market_type=s.market_type.value,
            signal_type=s.signal_type.value,
            entry_price=s.entry_price,
            stop_loss=s.stop_loss,
            take_profit=s.take_profit,
            confidence=s.confidence,
            status=s.status.value,
            created_at=s.created_at,
            closed_at=s.closed_at,
            pnl_percent=s.pnl_percent,
            alasan=s.alasan,
        )
        for s in signals
    ]


@router.get("/history")
async def get_signal_history(
    limit: int = Query(50, ge=1, le=500),
    symbol: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Ambil history sinyal dengan filter"""
    query = db.query(Signal)
    
    if symbol:
        query = query.filter(Signal.symbol == symbol.upper())
    
    if status:
        query = query.filter(Signal.status == SignalStatus[status])
    
    signals = query.order_by(Signal.created_at.desc()).limit(limit).all()
    
    return {
        "jumlah": len(signals),
        "signals": [
            {
                "id": s.id,
                "symbol": s.symbol,
                "market_type": s.market_type.value,
                "signal_type": s.signal_type.value,
                "entry_price": s.entry_price,
                "stop_loss": s.stop_loss,
                "take_profit": s.take_profit,
                "confidence": s.confidence,
                "status": s.status.value,
                "created_at": s.created_at.isoformat(),
                "closed_at": s.closed_at.isoformat() if s.closed_at else None,
                "pnl_percent": s.pnl_percent,
                "duration_minutes": s.duration_minutes,
                "alasan": s.alasan,
            }
            for s in signals
        ]
    }


@router.post("/close/{signal_id}")
async def close_signal(
    signal_id: int,
    exit_price: float = Query(..., gt=0),
    status: str = Query(..., description="HIT_TP, HIT_SL, atau EXPIRED"),
    db: Session = Depends(get_db)
):
    """Close sinyal secara manual"""
    signal = db.query(Signal).filter(Signal.id == signal_id).first()
    
    if not signal:
        raise HTTPException(status_code=404, detail="Sinyal tidak ditemukan")
    
    if signal.status != SignalStatus.OPEN:
        raise HTTPException(status_code=400, detail="Sinyal sudah ditutup")
    
    # Update signal
    signal.status = SignalStatus[status]
    signal.exit_price = exit_price
    signal.closed_at = datetime.utcnow()
    signal.pnl_percent = signal.calculate_pnl(exit_price)
    signal.duration_minutes = int((signal.closed_at - signal.created_at).total_seconds() / 60)
    
    db.commit()
    
    return {
        "status": "sukses",
        "message": f"Sinyal {signal_id} ditutup dengan status {status}",
        "pnl_percent": signal.pnl_percent
    }


@router.get("/statistics")
async def get_statistics(
    days: int = Query(7, ge=1, le=90),
    db: Session = Depends(get_db)
):
    """Ambil statistik sinyal"""
    from datetime import timedelta
    
    start_date = datetime.utcnow() - timedelta(days=days)
    
    signals = db.query(Signal).filter(
        Signal.created_at >= start_date
    ).all()
    
    total = len(signals)
    closed = [s for s in signals if s.status != SignalStatus.OPEN]
    hit_tp = len([s for s in closed if s.status == SignalStatus.HIT_TP])
    hit_sl = len([s for s in closed if s.status == SignalStatus.HIT_SL])
    
    win_rate = (hit_tp / len(closed) * 100) if closed else 0
    
    pnl_values = [s.pnl_percent for s in closed if s.pnl_percent is not None]
    avg_pnl = sum(pnl_values) / len(pnl_values) if pnl_values else 0
    total_pnl = sum(pnl_values)
    
    return {
        "periode_hari": days,
        "total_signals": total,
        "open": len([s for s in signals if s.status == SignalStatus.OPEN]),
        "closed": len(closed),
        "hit_tp": hit_tp,
        "hit_sl": hit_sl,
        "expired": len([s for s in closed if s.status == SignalStatus.EXPIRED]),
        "win_rate": round(win_rate, 2),
        "avg_pnl": round(avg_pnl, 2),
        "total_pnl": round(total_pnl, 2),
        "best_trade": max(pnl_values) if pnl_values else 0,
        "worst_trade": min(pnl_values) if pnl_values else 0,
    }


# ============================================================================
# FAVORITES ENDPOINTS
# ============================================================================

@router.post("/favorites/add")
async def add_favorite(fav: FavoriteCreate, db: Session = Depends(get_db)):
    """Tambah pair ke favorit"""
    existing = db.query(FavoritePair).filter(
        FavoritePair.symbol == fav.symbol.upper()
    ).first()
    
    if existing:
        if not existing.is_active:
            existing.is_active = True
            db.commit()
            return {"status": "sukses", "message": f"{fav.symbol} diaktifkan kembali"}
        raise HTTPException(status_code=400, detail="Pair sudah ada di favorit")
    
    new_fav = FavoritePair(
        symbol=fav.symbol.upper(),
        market_type=MarketType[fav.market_type]
    )
    db.add(new_fav)
    db.commit()
    
    return {"status": "sukses", "message": f"{fav.symbol} ditambahkan ke favorit"}


@router.delete("/favorites/{symbol}")
async def remove_favorite(symbol: str, db: Session = Depends(get_db)):
    """Hapus pair dari favorit"""
    fav = db.query(FavoritePair).filter(
        FavoritePair.symbol == symbol.upper()
    ).first()
    
    if not fav:
        raise HTTPException(status_code=404, detail="Pair tidak ditemukan")
    
    fav.is_active = False
    db.commit()
    
    return {"status": "sukses", "message": f"{symbol} dihapus dari favorit"}


@router.get("/favorites")
async def get_favorites(db: Session = Depends(get_db)):
    """Ambil semua pair favorit"""
    favorites = db.query(FavoritePair).filter(
        FavoritePair.is_active == True
    ).all()
    
    return {
        "jumlah": len(favorites),
        "favorites": [
            {
                "symbol": f.symbol,
                "market_type": f.market_type.value,
                "added_at": f.added_at.isoformat()
            }
            for f in favorites
        ]
    }
