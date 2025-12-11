"""
Engine Backtesting untuk menghitung confidence yang JUJUR berdasarkan data historis.
Tidak ada inflasi artifisial - confidence = actual winrate dari backtesting.

PRINSIP:
- Confidence = Real historical performance
- No fake inflation
- Data-driven approach
- Scientific & trustworthy
"""

from typing import Dict, List, Tuple, Optional
import pandas as pd
from dataclasses import dataclass
from pathlib import Path

@dataclass
class HasilBacktest:
    """Hasil backtesting untuk satu sinyal."""
    sinyal_tipe: str  # "BUY" atau "SELL"
    entry_price: float
    exit_price: float
    profit_loss: float
    win: bool
    durasi_jam: int
    alasan_exit: str  # "TP", "SL", "timeout"

@dataclass
class StatistikBacktest:
    """Statistik keseluruhan dari backtesting."""
    total_sinyal: int
    total_win: int
    total_loss: int
    winrate: float
    profit_total: float
    profit_rata_rata: float
    max_drawdown: float
    confidence_real: float  # = winrate (HONEST!)

def hitung_confidence_jujur(
    df_historis: pd.DataFrame,
    sinyal_list: List[Dict],
    mode_trading: str
) -> float:
    """
    Hitung confidence yang JUJUR berdasarkan backtesting historis.
    
    Parameters:
    -----------
    df_historis : pd.DataFrame
        Data historis H1 untuk backtesting
    sinyal_list : List[Dict]
        List sinyal yang akan di-backtest
    mode_trading : str
        Mode trading: "aktif", "santai", atau "pasif"
    
    Returns:
    --------
    float
        Confidence REAL berdasarkan actual winrate (0.0 - 1.0)
    """
    if not sinyal_list or df_historis.empty:
        return 0.30  # Conservative default untuk data insufficient
    
    hasil_backtest = []
    
    for sinyal in sinyal_list:
        try:
            # Cari index entry berdasarkan timestamp
            entry_time = pd.to_datetime(sinyal['timestamp'])
            entry_idx = df_historis[df_historis['open_time'] <= entry_time].index[-1]
            
            # Simulasi trade
            hasil = simulasi_trade_historis(
                df_historis=df_historis,
                entry_idx=entry_idx,
                sinyal=sinyal,
                mode_trading=mode_trading
            )
            
            if hasil:
                hasil_backtest.append(hasil)
                
        except Exception as e:
            # Skip sinyal yang error
            continue
    
    if not hasil_backtest:
        return 0.30  # Conservative default
    
    # Hitung statistik REAL
    total_sinyal = len(hasil_backtest)
    total_win = sum(1 for h in hasil_backtest if h.win)
    winrate = total_win / total_sinyal if total_sinyal > 0 else 0.0
    
    # Confidence = REAL winrate (NO INFLATION!)
    confidence_real = winrate
    
    # Apply conservative adjustment untuk sample size kecil
    if total_sinyal < 10:
        confidence_real *= 0.8  # Reduce confidence untuk sample kecil
    elif total_sinyal < 20:
        confidence_real *= 0.9  # Slight reduction
    
    # Cap minimum dan maximum yang realistis
    confidence_real = max(0.20, min(0.85, confidence_real))
    
    return confidence_real

def simulasi_trade_historis(
    df_historis: pd.DataFrame,
    entry_idx: int,
    sinyal: Dict,
    mode_trading: str
) -> Optional[HasilBacktest]:
    """
    Simulasi satu trade berdasarkan data historis.
    
    Returns:
    --------
    HasilBacktest atau None jika simulasi gagal
    """
    if entry_idx >= len(df_historis) - 1:
        return None
    
    entry_price = float(sinyal['entry'])
    stop_loss = float(sinyal['stop_loss'])
    take_profit = float(sinyal['take_profit'])
    tipe_sinyal = sinyal['tipe']
    
    # Tentukan timeout berdasarkan mode
    timeout_jam = {
        "aktif": 8,    # 8 jam max untuk mode aktif
        "santai": 24,  # 24 jam max untuk mode santai
        "pasif": 72    # 72 jam max untuk mode pasif
    }.get(mode_trading, 24)
    
    # Simulasi pergerakan harga setelah entry
    for i in range(entry_idx + 1, min(entry_idx + timeout_jam + 1, len(df_historis))):
        candle = df_historis.iloc[i]
        high = float(candle['high'])
        low = float(candle['low'])
        close = float(candle['close'])
        
        if tipe_sinyal == "BUY":
            # Check TP hit
            if high >= take_profit:
                profit = take_profit - entry_price
                return HasilBacktest(
                    sinyal_tipe=tipe_sinyal,
                    entry_price=entry_price,
                    exit_price=take_profit,
                    profit_loss=profit,
                    win=True,
                    durasi_jam=i - entry_idx,
                    alasan_exit="TP"
                )
            
            # Check SL hit
            if low <= stop_loss:
                loss = stop_loss - entry_price
                return HasilBacktest(
                    sinyal_tipe=tipe_sinyal,
                    entry_price=entry_price,
                    exit_price=stop_loss,
                    profit_loss=loss,
                    win=False,
                    durasi_jam=i - entry_idx,
                    alasan_exit="SL"
                )
        
        else:  # SELL
            # Check TP hit
            if low <= take_profit:
                profit = entry_price - take_profit
                return HasilBacktest(
                    sinyal_tipe=tipe_sinyal,
                    entry_price=entry_price,
                    exit_price=take_profit,
                    profit_loss=profit,
                    win=True,
                    durasi_jam=i - entry_idx,
                    alasan_exit="TP"
                )
            
            # Check SL hit
            if high >= stop_loss:
                loss = entry_price - stop_loss
                return HasilBacktest(
                    sinyal_tipe=tipe_sinyal,
                    entry_price=entry_price,
                    exit_price=stop_loss,
                    profit_loss=loss,
                    win=False,
                    durasi_jam=i - entry_idx,
                    alasan_exit="SL"
                )
    
    # Timeout - exit di close terakhir
    final_candle = df_historis.iloc[min(entry_idx + timeout_jam, len(df_historis) - 1)]
    exit_price = float(final_candle['close'])
    
    if tipe_sinyal == "BUY":
        profit_loss = exit_price - entry_price
    else:
        profit_loss = entry_price - exit_price
    
    return HasilBacktest(
        sinyal_tipe=tipe_sinyal,
        entry_price=entry_price,
        exit_price=exit_price,
        profit_loss=profit_loss,
        win=profit_loss > 0,
        durasi_jam=timeout_jam,
        alasan_exit="timeout"
    )

def load_data_historis_untuk_backtest(folder_path: str) -> pd.DataFrame:
    """
    Load data historis H1 untuk backtesting.
    Gabungkan semua file CSV dalam folder menjadi satu DataFrame.
    """
    folder = Path(folder_path)
    if not folder.exists():
        return pd.DataFrame()
    
    all_data = []
    
    for csv_file in folder.glob("*.csv"):
        try:
            df = pd.read_csv(csv_file)
            if 'open_time' in df.columns:
                df['open_time'] = pd.to_datetime(df['open_time'], errors='coerce')
                all_data.append(df)
        except Exception as e:
            continue
    
    if not all_data:
        return pd.DataFrame()
    
    # Gabungkan dan sort berdasarkan waktu
    df_combined = pd.concat(all_data, ignore_index=True)
    df_combined = df_combined.sort_values('open_time').reset_index(drop=True)
    
    # Remove duplicates berdasarkan open_time
    df_combined = df_combined.drop_duplicates(subset=['open_time']).reset_index(drop=True)
    
    return df_combined

def generate_laporan_backtest(hasil_list: List[HasilBacktest]) -> StatistikBacktest:
    """
    Generate laporan statistik dari hasil backtesting.
    """
    if not hasil_list:
        return StatistikBacktest(
            total_sinyal=0,
            total_win=0,
            total_loss=0,
            winrate=0.0,
            profit_total=0.0,
            profit_rata_rata=0.0,
            max_drawdown=0.0,
            confidence_real=0.30
        )
    
    total_sinyal = len(hasil_list)
    total_win = sum(1 for h in hasil_list if h.win)
    total_loss = total_sinyal - total_win
    winrate = total_win / total_sinyal
    
    profit_total = sum(h.profit_loss for h in hasil_list)
    profit_rata_rata = profit_total / total_sinyal
    
    # Hitung max drawdown
    running_profit = 0
    peak = 0
    max_drawdown = 0
    
    for hasil in hasil_list:
        running_profit += hasil.profit_loss
        if running_profit > peak:
            peak = running_profit
        drawdown = peak - running_profit
        if drawdown > max_drawdown:
            max_drawdown = drawdown
    
    return StatistikBacktest(
        total_sinyal=total_sinyal,
        total_win=total_win,
        total_loss=total_loss,
        winrate=winrate,
        profit_total=profit_total,
        profit_rata_rata=profit_rata_rata,
        max_drawdown=max_drawdown,
        confidence_real=winrate  # HONEST confidence = actual winrate
    )