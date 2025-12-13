"""
Auto Signal Generator Service.
Service untuk generate sinyal trading secara otomatis dan track SL/TP real-time.
Menggunakan Binance WebSocket untuk update harga setiap detik.
"""

import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import aiohttp

from ..models import (
    SessionLocal, Signal, SignalStatus, SignalType, MarketType
)


class AutoSignalService:
    """
    Service untuk auto-generate sinyal dan track SL/TP secara real-time.
    Menggunakan WebSocket Binance untuk harga real-time.
    """
    
    def __init__(self):
        self.is_running = False
        self.tracked_signals: Dict[int, dict] = {}
        self.current_prices: Dict[str, float] = {}  # symbol -> price
        self.check_interval = 5  # cek database setiap 5 detik
        self.last_check = None
        self.ws_task = None
        self.tracking_task = None
        self.stats = {
            "total_checked": 0,
            "total_closed": 0,
            "hit_tp": 0,
            "hit_sl": 0,
            "expired": 0,
        }
        
    async def start(self):
        """Mulai auto signal service dengan WebSocket"""
        if self.is_running:
            return {"status": "sudah_berjalan", "pesan": "Service sudah aktif"}
        
        self.is_running = True
        
        # Start tracking loop
        self.tracking_task = asyncio.create_task(self._tracking_loop())
        
        # Start WebSocket untuk real-time prices
        self.ws_task = asyncio.create_task(self._websocket_loop())
        
        return {"status": "dimulai", "pesan": "Auto signal service dimulai dengan real-time tracking"}
    
    async def stop(self):
        """Stop auto signal service"""
        self.is_running = False
        
        # Cancel tasks
        if self.ws_task:
            self.ws_task.cancel()
        if self.tracking_task:
            self.tracking_task.cancel()
            
        return {"status": "dihentikan", "pesan": "Auto signal service dihentikan"}
    
    async def get_status(self):
        """Ambil status service"""
        return {
            "is_running": self.is_running,
            "tracked_signals": len(self.tracked_signals),
            "symbols_tracked": list(self.current_prices.keys()),
            "last_check": self.last_check.isoformat() if self.last_check else None,
            "check_interval": self.check_interval,
            "stats": self.stats,
        }
    
    async def _websocket_loop(self):
        """WebSocket loop untuk real-time price updates dari Binance"""
        while self.is_running:
            try:
                # Get symbols yang perlu di-track
                symbols = await self._get_tracked_symbols()
                
                if not symbols:
                    await asyncio.sleep(5)
                    continue
                
                # Build WebSocket URL
                streams = "/".join([f"{s.lower()}@ticker" for s in symbols])
                ws_url = f"wss://stream.binance.com:9443/stream?streams={streams}"
                
                async with aiohttp.ClientSession() as session:
                    async with session.ws_connect(ws_url) as ws:
                        print(f"[AutoSignal] WebSocket connected, tracking {len(symbols)} symbols")
                        
                        async for msg in ws:
                            if not self.is_running:
                                break
                                
                            if msg.type == aiohttp.WSMsgType.TEXT:
                                try:
                                    data = json.loads(msg.data)
                                    if "data" in data:
                                        ticker = data["data"]
                                        symbol = ticker.get("s")
                                        price = float(ticker.get("c", 0))
                                        
                                        if symbol and price > 0:
                                            self.current_prices[symbol] = price
                                            
                                            # Immediate check untuk symbol ini
                                            await self._check_signal_for_symbol(symbol, price)
                                except:
                                    pass
                            elif msg.type == aiohttp.WSMsgType.ERROR:
                                break
                                
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"[AutoSignal] WebSocket error: {e}")
                await asyncio.sleep(5)
    
    async def _get_tracked_symbols(self) -> List[str]:
        """Ambil list symbols yang sedang di-track"""
        db = SessionLocal()
        try:
            signals = db.query(Signal.symbol).filter(
                Signal.status == SignalStatus.OPEN
            ).distinct().all()
            return [s[0] for s in signals]
        finally:
            db.close()
    
    async def _check_signal_for_symbol(self, symbol: str, current_price: float):
        """Cek sinyal untuk symbol tertentu secara real-time"""
        db = SessionLocal()
        try:
            signals = db.query(Signal).filter(
                Signal.symbol == symbol,
                Signal.status == SignalStatus.OPEN
            ).all()
            
            for signal in signals:
                # Update highest/lowest
                if current_price > (signal.highest_price or 0):
                    signal.highest_price = current_price
                if signal.lowest_price is None or current_price < signal.lowest_price:
                    signal.lowest_price = current_price
                
                # Cek SL/TP
                hit_result = self._check_sl_tp(signal, current_price)
                
                if hit_result:
                    self._close_signal(signal, current_price, hit_result["status"])
                    self.stats["total_closed"] += 1
                    
                    if hit_result["status"] == SignalStatus.HIT_TP:
                        self.stats["hit_tp"] += 1
                    else:
                        self.stats["hit_sl"] += 1
            
            db.commit()
            
        except Exception as e:
            print(f"[AutoSignal] Check error: {e}")
            db.rollback()
        finally:
            db.close()
    
    async def _tracking_loop(self):
        """Loop backup untuk tracking sinyal (fallback jika WS mati)"""
        while self.is_running:
            try:
                await self._check_open_signals()
                await self._check_expired_signals_auto()
                self.last_check = datetime.utcnow()
                self.stats["total_checked"] += 1
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"[AutoSignal] Tracking error: {e}")
            
            await asyncio.sleep(self.check_interval)
    
    async def _check_open_signals(self):
        """Cek semua sinyal OPEN dan update status jika kena SL/TP"""
        db = SessionLocal()
        try:
            open_signals = db.query(Signal).filter(
                Signal.status == SignalStatus.OPEN
            ).all()
            
            if not open_signals:
                return
            
            # Ambil harga terkini untuk symbols yang belum ada di cache
            symbols_to_fetch = [
                s.symbol for s in open_signals 
                if s.symbol not in self.current_prices
            ]
            
            if symbols_to_fetch:
                prices = await self._get_current_prices(symbols_to_fetch)
                self.current_prices.update(prices)
            
            for signal in open_signals:
                current_price = self.current_prices.get(signal.symbol)
                if not current_price:
                    continue
                
                # Update highest/lowest
                if current_price > (signal.highest_price or 0):
                    signal.highest_price = current_price
                if signal.lowest_price is None or current_price < signal.lowest_price:
                    signal.lowest_price = current_price
                
                # Cek SL/TP
                hit_result = self._check_sl_tp(signal, current_price)
                
                if hit_result:
                    self._close_signal(signal, current_price, hit_result["status"])
            
            db.commit()
            
        finally:
            db.close()
    
    def _close_signal(self, signal: Signal, exit_price: float, status: SignalStatus):
        """Close signal dengan status tertentu"""
        signal.status = status
        signal.exit_price = exit_price
        signal.closed_at = datetime.utcnow()
        signal.pnl_percent = signal.calculate_pnl(exit_price)
        signal.duration_minutes = int(
            (signal.closed_at - signal.created_at).total_seconds() / 60
        )
        
        pnl_str = f"+{signal.pnl_percent:.2f}%" if signal.pnl_percent >= 0 else f"{signal.pnl_percent:.2f}%"
        print(f"[AutoSignal] {signal.symbol} {status.value} @ {exit_price} | PnL: {pnl_str}")
    
    def _check_sl_tp(self, signal: Signal, current_price: float) -> Optional[dict]:
        """Cek apakah harga sudah kena SL atau TP"""
        if signal.signal_type == SignalType.BELI:
            if current_price >= signal.take_profit:
                return {"status": SignalStatus.HIT_TP}
            elif current_price <= signal.stop_loss:
                return {"status": SignalStatus.HIT_SL}
        else:
            if current_price <= signal.take_profit:
                return {"status": SignalStatus.HIT_TP}
            elif current_price >= signal.stop_loss:
                return {"status": SignalStatus.HIT_SL}
        return None
    
    async def _get_current_prices(self, symbols: List[str]) -> Dict[str, float]:
        """Ambil harga terkini dari Binance API"""
        prices = {}
        
        try:
            async with aiohttp.ClientSession() as session:
                # Batch request untuk semua symbols
                url = "https://api.binance.com/api/v3/ticker/price"
                async with session.get(url, timeout=10) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        for item in data:
                            if item["symbol"] in symbols:
                                prices[item["symbol"]] = float(item["price"])
        except Exception as e:
            print(f"[AutoSignal] Price fetch error: {e}")
        
        return prices
    
    async def _check_expired_signals_auto(self):
        """Auto-check expired signals setiap loop"""
        db = SessionLocal()
        try:
            # Sinyal expired setelah 24 jam untuk mode santai, 48 jam untuk pasif
            cutoff_santai = datetime.utcnow() - timedelta(hours=24)
            cutoff_pasif = datetime.utcnow() - timedelta(hours=48)
            
            expired = db.query(Signal).filter(
                Signal.status == SignalStatus.OPEN,
                Signal.created_at < cutoff_santai
            ).all()
            
            for signal in expired:
                # Cek mode trading untuk cutoff yang berbeda
                if signal.mode_trading == "pasif" and signal.created_at >= cutoff_pasif:
                    continue
                    
                signal.status = SignalStatus.EXPIRED
                signal.closed_at = datetime.utcnow()
                signal.duration_minutes = int(
                    (signal.closed_at - signal.created_at).total_seconds() / 60
                )
                self.stats["expired"] += 1
                print(f"[AutoSignal] {signal.symbol} EXPIRED")
            
            db.commit()
        finally:
            db.close()
    
    async def check_expired_signals(self, max_hours: int = 24):
        """Manual check expired signals"""
        db = SessionLocal()
        try:
            cutoff = datetime.utcnow() - timedelta(hours=max_hours)
            
            expired = db.query(Signal).filter(
                Signal.status == SignalStatus.OPEN,
                Signal.created_at < cutoff
            ).all()
            
            for signal in expired:
                signal.status = SignalStatus.EXPIRED
                signal.closed_at = datetime.utcnow()
                signal.duration_minutes = int(
                    (signal.closed_at - signal.created_at).total_seconds() / 60
                )
            
            db.commit()
            return {"expired_count": len(expired)}
            
        finally:
            db.close()
    
    def get_current_price(self, symbol: str) -> Optional[float]:
        """Get cached current price untuk symbol"""
        return self.current_prices.get(symbol)


# Singleton instance
auto_signal_service = AutoSignalService()
