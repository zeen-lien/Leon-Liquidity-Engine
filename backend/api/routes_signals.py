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
from ..services.auto_signal import auto_signal_service

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
    # Entry size untuk tracking profit/loss dalam dollar
    modal_total: Optional[float] = Field(None, description="Total modal user")
    entry_pct: Optional[float] = Field(None, description="Persentase entry dari modal")
    entry_amount: Optional[float] = Field(None, description="Jumlah dollar yang dientry")


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
    
    RULE: Satu symbol bisa punya multiple signals TAPI harus beda mode_trading.
    Contoh: BTCUSDT bisa punya sinyal AKTIF, SANTAI, dan PASIF sekaligus.
    """
    # Cek apakah ada sinyal OPEN untuk symbol DAN mode yang sama
    existing = db.query(Signal).filter(
        Signal.symbol == signal.symbol.upper(),
        Signal.mode_trading == signal.mode_trading,
        Signal.status == SignalStatus.OPEN
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Sudah ada sinyal OPEN untuk {signal.symbol} mode {signal.mode_trading.upper()}. Tunggu sampai kena SL/TP atau gunakan mode lain."
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
        # Entry size untuk tracking profit/loss dalam dollar
        modal_total=signal.modal_total,
        entry_pct=signal.entry_pct,
        entry_amount=signal.entry_amount,
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


# Duplicate endpoint removed - using the comprehensive one below


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


# ============================================================================
# AUTO SIGNAL & TRACKING ENDPOINTS
# ============================================================================

@router.post("/auto/start")
async def start_auto_signal():
    """Mulai auto signal tracking service"""
    result = await auto_signal_service.start()
    return result


@router.post("/auto/stop")
async def stop_auto_signal():
    """Stop auto signal tracking service"""
    result = await auto_signal_service.stop()
    return result


@router.get("/auto/status")
async def get_auto_signal_status():
    """Ambil status auto signal service"""
    result = await auto_signal_service.get_status()
    return result


@router.post("/auto/check-expired")
async def check_expired_signals(max_hours: int = Query(24, ge=1, le=168)):
    """Cek dan tutup sinyal yang sudah expired"""
    result = await auto_signal_service.check_expired_signals(max_hours)
    return result


@router.get("/tracking/live")
async def get_live_tracking(db: Session = Depends(get_db)):
    """
    Ambil semua sinyal OPEN dengan info tracking real-time.
    Endpoint ini digunakan untuk display Active Signals di frontend.
    """
    signals = db.query(Signal).filter(
        Signal.status == SignalStatus.OPEN
    ).order_by(Signal.created_at.desc()).all()
    
    result = []
    for s in signals:
        # Hitung durasi sejak entry
        duration = datetime.utcnow() - s.created_at
        hours = int(duration.total_seconds() / 3600)
        minutes = int((duration.total_seconds() % 3600) / 60)
        
        # Hitung jarak ke SL dan TP dalam persen
        if s.signal_type == SignalType.BELI:
            sl_distance = ((s.entry_price - s.stop_loss) / s.entry_price) * 100
            tp_distance = ((s.take_profit - s.entry_price) / s.entry_price) * 100
        else:
            sl_distance = ((s.stop_loss - s.entry_price) / s.entry_price) * 100
            tp_distance = ((s.entry_price - s.take_profit) / s.entry_price) * 100
        
        result.append({
            "id": s.id,
            "symbol": s.symbol,
            "market_type": s.market_type.value,
            "signal_type": s.signal_type.value,
            "mode_trading": s.mode_trading,
            "entry_price": s.entry_price,
            "stop_loss": s.stop_loss,
            "take_profit": s.take_profit,
            "confidence": s.confidence,
            "created_at": s.created_at.isoformat(),
            "duration": f"{hours}j {minutes}m",
            "duration_minutes": int(duration.total_seconds() / 60),
            "sl_distance_pct": round(sl_distance, 2),
            "tp_distance_pct": round(tp_distance, 2),
            "highest_price": s.highest_price,
            "lowest_price": s.lowest_price,
            "alasan": s.alasan,
            # Entry size untuk tracking profit/loss dalam dollar
            "modal_total": s.modal_total,
            "entry_pct": s.entry_pct,
            "entry_amount": s.entry_amount,
        })
    
    return {
        "jumlah": len(result),
        "signals": result,
        "auto_tracking": await auto_signal_service.get_status(),
    }


# ============================================================================
# PERFORMANCE & ANALYTICS ENDPOINTS
# ============================================================================

@router.get("/performance/summary")
async def get_performance_summary(db: Session = Depends(get_db)):
    """
    Ambil ringkasan performa sinyal secara keseluruhan.
    Termasuk win rate, profit factor, dan statistik lainnya.
    """
    from datetime import timedelta
    
    # All time stats
    all_signals = db.query(Signal).all()
    closed_signals = [s for s in all_signals if s.status != SignalStatus.OPEN]
    
    # Calculate metrics
    total = len(all_signals)
    total_closed = len(closed_signals)
    hit_tp = len([s for s in closed_signals if s.status == SignalStatus.HIT_TP])
    hit_sl = len([s for s in closed_signals if s.status == SignalStatus.HIT_SL])
    expired = len([s for s in closed_signals if s.status == SignalStatus.EXPIRED])
    
    # Win rate
    win_rate = (hit_tp / total_closed * 100) if total_closed > 0 else 0
    
    # P&L calculations
    pnl_values = [s.pnl_percent for s in closed_signals if s.pnl_percent is not None]
    total_pnl = sum(pnl_values) if pnl_values else 0
    avg_pnl = total_pnl / len(pnl_values) if pnl_values else 0
    
    # Profit factor (total profit / total loss)
    profits = [p for p in pnl_values if p > 0]
    losses = [abs(p) for p in pnl_values if p < 0]
    profit_factor = sum(profits) / sum(losses) if losses else float('inf') if profits else 0
    
    # Best and worst trades
    best_trade = max(pnl_values) if pnl_values else 0
    worst_trade = min(pnl_values) if pnl_values else 0
    
    # Average duration
    durations = [s.duration_minutes for s in closed_signals if s.duration_minutes]
    avg_duration = sum(durations) / len(durations) if durations else 0
    
    # Last 7 days performance
    week_ago = datetime.utcnow() - timedelta(days=7)
    recent_signals = [s for s in closed_signals if s.closed_at and s.closed_at >= week_ago]
    recent_tp = len([s for s in recent_signals if s.status == SignalStatus.HIT_TP])
    recent_sl = len([s for s in recent_signals if s.status == SignalStatus.HIT_SL])
    recent_win_rate = (recent_tp / len(recent_signals) * 100) if recent_signals else 0
    
    return {
        "all_time": {
            "total_signals": total,
            "total_closed": total_closed,
            "open": total - total_closed,
            "hit_tp": hit_tp,
            "hit_sl": hit_sl,
            "expired": expired,
            "win_rate": round(win_rate, 2),
            "total_pnl": round(total_pnl, 2),
            "avg_pnl": round(avg_pnl, 2),
            "profit_factor": round(profit_factor, 2) if profit_factor != float('inf') else "∞",
            "best_trade": round(best_trade, 2),
            "worst_trade": round(worst_trade, 2),
            "avg_duration_minutes": round(avg_duration, 0),
        },
        "last_7_days": {
            "total": len(recent_signals),
            "hit_tp": recent_tp,
            "hit_sl": recent_sl,
            "win_rate": round(recent_win_rate, 2),
        },
        "tracking_status": await auto_signal_service.get_status(),
    }


@router.get("/performance/history")
async def get_performance_history(
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """
    Ambil history performa sinyal per hari untuk chart.
    """
    from datetime import timedelta
    from collections import defaultdict
    
    start_date = datetime.utcnow() - timedelta(days=days)
    
    signals = db.query(Signal).filter(
        Signal.closed_at >= start_date,
        Signal.status != SignalStatus.OPEN
    ).all()
    
    # Group by date
    daily_stats = defaultdict(lambda: {"tp": 0, "sl": 0, "expired": 0, "pnl": 0})
    
    for s in signals:
        if s.closed_at:
            date_key = s.closed_at.strftime("%Y-%m-%d")
            if s.status == SignalStatus.HIT_TP:
                daily_stats[date_key]["tp"] += 1
            elif s.status == SignalStatus.HIT_SL:
                daily_stats[date_key]["sl"] += 1
            else:
                daily_stats[date_key]["expired"] += 1
            
            if s.pnl_percent:
                daily_stats[date_key]["pnl"] += s.pnl_percent
    
    # Convert to list sorted by date
    history = []
    for date_str in sorted(daily_stats.keys()):
        stats = daily_stats[date_str]
        total = stats["tp"] + stats["sl"] + stats["expired"]
        win_rate = (stats["tp"] / total * 100) if total > 0 else 0
        history.append({
            "date": date_str,
            "total": total,
            "hit_tp": stats["tp"],
            "hit_sl": stats["sl"],
            "expired": stats["expired"],
            "win_rate": round(win_rate, 2),
            "pnl": round(stats["pnl"], 2),
        })
    
    return {
        "periode_hari": days,
        "history": history,
    }


@router.get("/realtime/prices")
async def get_realtime_prices():
    """
    Ambil cached real-time prices dari auto signal service.
    Prices di-update via WebSocket setiap detik.
    """
    return {
        "prices": auto_signal_service.current_prices,
        "last_update": auto_signal_service.last_check.isoformat() if auto_signal_service.last_check else None,
        "is_tracking": auto_signal_service.is_running,
    }


@router.delete("/delete/{signal_id}")
async def delete_signal(signal_id: int, db: Session = Depends(get_db)):
    """Hapus sinyal dari database"""
    signal = db.query(Signal).filter(Signal.id == signal_id).first()
    
    if not signal:
        raise HTTPException(status_code=404, detail="Sinyal tidak ditemukan")
    
    db.delete(signal)
    db.commit()
    
    return {"status": "sukses", "message": f"Sinyal {signal_id} dihapus"}


@router.get("/history")
async def get_signal_history(
    status: Optional[str] = Query(None, description="Filter by status: HIT_TP, HIT_SL, EXPIRED, CANCELLED"),
    market_type: Optional[str] = Query(None, description="Filter by market: SPOT, FUTURES"),
    signal_type: Optional[str] = Query(None, description="Filter by type: BELI, JUAL"),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db)
):
    """
    Ambil riwayat sinyal yang sudah closed (HIT_TP, HIT_SL, EXPIRED, CANCELLED).
    Dengan filter dan statistik.
    """
    # Base query - exclude OPEN signals
    query = db.query(Signal).filter(Signal.status != SignalStatus.OPEN)
    
    # Apply filters
    if status and status != 'all':
        try:
            query = query.filter(Signal.status == SignalStatus[status])
        except KeyError:
            pass
    
    if market_type and market_type != 'all':
        try:
            query = query.filter(Signal.market_type == MarketType[market_type])
        except KeyError:
            pass
    
    if signal_type and signal_type != 'all':
        try:
            query = query.filter(Signal.signal_type == SignalType[signal_type])
        except KeyError:
            pass
    
    # Get signals ordered by closed_at desc
    signals = query.order_by(Signal.closed_at.desc()).limit(limit).all()
    
    # Calculate stats
    all_closed = db.query(Signal).filter(Signal.status != SignalStatus.OPEN).all()
    hit_tp = len([s for s in all_closed if s.status == SignalStatus.HIT_TP])
    hit_sl = len([s for s in all_closed if s.status == SignalStatus.HIT_SL])
    total_closed = len(all_closed)
    win_rate = (hit_tp / total_closed * 100) if total_closed > 0 else 0
    
    # Calculate profit/loss in dollars
    total_profit = 0
    total_loss = 0
    for s in all_closed:
        if s.pnl_percent and s.entry_amount:
            pnl_dollar = s.entry_amount * (s.pnl_percent / 100)
            if pnl_dollar > 0:
                total_profit += pnl_dollar
            else:
                total_loss += abs(pnl_dollar)
    
    # Format signals for response
    result = []
    for s in signals:
        # Calculate P&L in dollars
        pnl_dollar = 0
        if s.pnl_percent and s.entry_amount:
            pnl_dollar = s.entry_amount * (s.pnl_percent / 100)
        
        # Format duration
        duration_str = "-"
        if s.duration_minutes:
            hours = s.duration_minutes // 60
            mins = s.duration_minutes % 60
            duration_str = f"{hours}j {mins}m"
        
        result.append({
            "id": s.id,
            "symbol": s.symbol,
            "market_type": s.market_type.value,
            "signal_type": s.signal_type.value,
            "mode_trading": s.mode_trading,
            "entry_price": s.entry_price,
            "exit_price": s.exit_price,
            "stop_loss": s.stop_loss,
            "take_profit": s.take_profit,
            "status": s.status.value,
            "pnl_percent": s.pnl_percent,
            "pnl_dollar": round(pnl_dollar, 2),
            "entry_amount": s.entry_amount,
            "created_at": s.created_at.isoformat() if s.created_at else None,
            "closed_at": s.closed_at.isoformat() if s.closed_at else None,
            "duration": duration_str,
            "confidence": s.confidence,
        })
    
    return {
        "status": "sukses",
        "stats": {
            "total_closed": total_closed,
            "hit_tp": hit_tp,
            "hit_sl": hit_sl,
            "win_rate": round(win_rate, 1),
            "total_profit": round(total_profit, 2),
            "total_loss": round(total_loss, 2),
        },
        "signals": result,
    }
