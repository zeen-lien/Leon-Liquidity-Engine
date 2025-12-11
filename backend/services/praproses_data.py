"""
Modul preprocessing untuk Leon Liquidity Engine.
Di sini kita menghitung semua indikator KLASIK yang dibutuhkan oleh
mode trading (Aktif / Santai / Pasif) di signal generator.

PERIODE INDIKATOR YANG DIHITUNG (FIXED):
- RSI: 6, 8, 10, 14
- EMA : 9, 20, 50, 200
- ATR : 14
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List

import pandas as pd

# Periode indikator yang FIXED (tidak bisa diubah)
PERIODE_RSI_AKTIF: int = 6
PERIODE_RSI_INTRADAY_1: int = 8
PERIODE_RSI_INTRADAY_2: int = 10
PERIODE_RSI_SWING: int = 14

# EMA untuk berbagai trading style
PERIODE_EMA_9: int = 9      # Mode aktif micro trend
PERIODE_EMA_20: int = 20    # Short / pullback zone
PERIODE_EMA_50: int = 50    # Mid trend
PERIODE_EMA_200: int = 200  # Macro trend (trend filter)

PERIODE_ATR: int = 14


def hitung_rsi(kolom_tutup: pd.Series, periode: int = 14) -> pd.Series:
    """
    Hitung indikator Relative Strength Index (RSI) menggunakan EMA.
    """
    perubahan = kolom_tutup.diff()
    kenaikan = perubahan.clip(lower=0)
    penurunan = (-perubahan).clip(lower=0)

    rata_naik = kenaikan.ewm(alpha=1 / periode, adjust=False).mean()
    rata_turun = penurunan.ewm(alpha=1 / periode, adjust=False).mean()

    rs = rata_naik / rata_turun.replace(0, pd.NA)
    rsi = 100 - (100 / (1 + rs))
    # Fix: Handle NaN/NaT dengan fillna dulu sebelum astype
    rsi = rsi.fillna(50.0)  # Default RSI 50 (neutral)
    # Pastikan semua values adalah numeric
    rsi = pd.to_numeric(rsi, errors='coerce').fillna(50.0)
    return rsi


def hitung_ema(kolom_tutup: pd.Series, periode: int = 50) -> pd.Series:
    """
    Hitung Exponential Moving Average (EMA).
    """
    # Handle NaN values
    ema = kolom_tutup.ewm(span=periode, adjust=False).mean()
    # Fill NaN dengan forward fill, lalu backward fill
    ema = ema.fillna(method='ffill').fillna(method='bfill')
    return ema


def hitung_atr(
    tinggi: pd.Series, rendah: pd.Series, tutup_sebelumnya: pd.Series, periode: int = 14
) -> pd.Series:
    """
    Hitung Average True Range (ATR) sederhana.

    True Range = max(
        high - low,
        abs(high - close_prev),
        abs(low - close_prev)
    )
    Lalu di-smoothing dengan EMA.
    """
    jarak_hl = tinggi - rendah
    jarak_hc = (tinggi - tutup_sebelumnya).abs()
    jarak_lc = (rendah - tutup_sebelumnya).abs()
    true_range = pd.concat([jarak_hl, jarak_hc, jarak_lc], axis=1).max(axis=1)
    atr = true_range.ewm(span=periode, adjust=False).mean()
    return atr


def tambah_indikator_ke_df(data_ohlcv: pd.DataFrame) -> pd.DataFrame:
    """
    Tambahkan semua indikator yang dibutuhkan ke DataFrame yang sudah terurut berdasarkan waktu.

    Indikator yang dihitung:
    - RSI 6, 8, 10, 14
    - Smoothing RSI (MA 3) untuk RSI 8 dan 10
    - EMA 9, 20, 50, 200
    - ATR 14
    - Candle structure (body, range, wick, return, volatility)
    - Distance to EMA, RSI position, Volume anomaly

    Parameters
    ----------
    data_ohlcv : pd.DataFrame
        DataFrame dengan kolom minimal: open_time, open, high, low, close, volume

    Returns
    -------
    pd.DataFrame
        DataFrame dengan kolom tambahan:
        rsi_6, rsi_8, rsi_10, rsi_14,
        rsi_8_ma3, rsi_10_ma3,
        ema_9, ema_20, ema_50, ema_200,
        atr_14,
        candle_body, candle_range, upper_wick, lower_wick,
        return_1, return_5, volatility_5,
        distance_to_ema_20, distance_to_ema_50,
        rsi_position, volume_anomaly
    """
    df = data_ohlcv.copy()
    df = df.sort_values("open_time")

    # -----------------------------
    # HITUNG RSI
    # -----------------------------
    df["rsi_6"] = hitung_rsi(df["close"], periode=PERIODE_RSI_AKTIF)
    df["rsi_8"] = hitung_rsi(df["close"], periode=PERIODE_RSI_INTRADAY_1)
    df["rsi_10"] = hitung_rsi(df["close"], periode=PERIODE_RSI_INTRADAY_2)
    df["rsi_14"] = hitung_rsi(df["close"], periode=PERIODE_RSI_SWING)

    # Smoothing RSI (MA 3) untuk intraday
    df["rsi_8_ma3"] = df["rsi_8"].rolling(window=3, min_periods=1).mean()
    df["rsi_10_ma3"] = df["rsi_10"].rolling(window=3, min_periods=1).mean()

    # -----------------------------
    # HITUNG EMA
    # -----------------------------
    df[f"ema_{PERIODE_EMA_9}"] = hitung_ema(df["close"], periode=PERIODE_EMA_9)
    df[f"ema_{PERIODE_EMA_20}"] = hitung_ema(df["close"], periode=PERIODE_EMA_20)
    df[f"ema_{PERIODE_EMA_50}"] = hitung_ema(df["close"], periode=PERIODE_EMA_50)
    df[f"ema_{PERIODE_EMA_200}"] = hitung_ema(df["close"], periode=PERIODE_EMA_200)

    # -----------------------------
    # HITUNG ATR 14
    # -----------------------------
    tutup_shift = df["close"].shift(1).fillna(df["close"])
    df["atr_14"] = hitung_atr(df["high"], df["low"], tutup_shift, periode=PERIODE_ATR)

    # -----------------------------
    # FITUR CANDLE STRUCTURE (untuk ML dan analisis lebih baik)
    # -----------------------------
    # Candle body = close - open
    df["candle_body"] = df["close"] - df["open"]
    
    # Candle range = high - low
    df["candle_range"] = df["high"] - df["low"]
    
    # Upper wick = high - max(open, close)
    df["upper_wick"] = df["high"] - df[["open", "close"]].max(axis=1)
    
    # Lower wick = min(open, close) - low
    df["lower_wick"] = df[["open", "close"]].min(axis=1) - df["low"]
    
    # Return 1 bar = (close/close.shift(1)) - 1
    df["return_1"] = (df["close"] / df["close"].shift(1).fillna(df["close"])) - 1.0
    
    # Return 5 bar = (close/close.shift(5)) - 1
    df["return_5"] = (df["close"] / df["close"].shift(5).fillna(df["close"])) - 1.0
    
    # Volatility 5 = rolling std dari return_1 dalam window 5
    df["volatility_5"] = df["return_1"].rolling(window=5, min_periods=1).std().fillna(0.0)
    
    # Distance to EMA 20 = close - ema_20
    df["distance_to_ema_20"] = df["close"] - df[f"ema_{PERIODE_EMA_20}"]
    
    # Distance to EMA 50 = close - ema_50
    df["distance_to_ema_50"] = df["close"] - df[f"ema_{PERIODE_EMA_50}"]
    
    # RSI position = rsi_14 / 100 (normalisasi 0-1)
    df["rsi_position"] = df["rsi_14"] / 100.0
    
    # Volume anomaly = volume / rolling_mean(volume, 20)
    if "volume" in df.columns:
        volume_mean_20 = df["volume"].rolling(window=20, min_periods=1).mean()
        df["volume_anomaly"] = df["volume"] / volume_mean_20.replace(0, 1.0)
    else:
        df["volume_anomaly"] = 1.0

    return df


def simpan_hasil_preprocess(df: pd.DataFrame, nama_berkas: str, folder_tujuan: Path) -> Path:
    """
    Simpan DataFrame hasil preprocessing ke folder tujuan (format CSV).
    Dipilih CSV agar tidak perlu dependency tambahan seperti pyarrow/fastparquet.
    
    Pastikan timestamp disimpan dengan benar (ISO format atau timestamp milidetik).
    """
    folder_tujuan.mkdir(parents=True, exist_ok=True)
    nama_output = Path(nama_berkas).with_suffix(".processed.csv")
    path_output = folder_tujuan / nama_output.name
    
    # Pastikan open_time disimpan dengan benar
    df_save = df.copy()
    if "open_time" in df_save.columns:
        # Jika open_time adalah datetime, simpan sebagai ISO format string
        if pd.api.types.is_datetime64_any_dtype(df_save["open_time"]):
            df_save["open_time"] = df_save["open_time"].dt.strftime("%Y-%m-%d %H:%M:%S")
        # Jika masih string tapi format salah, coba convert dulu
        elif df_save["open_time"].dtype == "object":
            try:
                # Coba parse sebagai datetime dulu
                df_save["open_time"] = pd.to_datetime(df_save["open_time"], errors="coerce", utc=True)
                df_save["open_time"] = df_save["open_time"].dt.strftime("%Y-%m-%d %H:%M:%S")
            except:
                pass
    
    # Simpan close_time sebagai integer (timestamp milidetik) jika ada
    if "close_time" in df_save.columns:
        # Pastikan close_time adalah integer (timestamp milidetik)
        if not pd.api.types.is_integer_dtype(df_save["close_time"]):
            try:
                df_save["close_time"] = pd.to_numeric(df_save["close_time"], errors="coerce").fillna(0).astype(int)
            except:
                pass
    
    df_save.to_csv(path_output, index=False)
    return path_output


def resample_ohlcv(df: pd.DataFrame, timeframe: str) -> pd.DataFrame:
    """
    Resample DataFrame OHLCV ke timeframe yang lebih besar.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame dengan kolom: open_time, open, high, low, close, volume
        open_time harus sudah dalam format datetime.
    timeframe : str
        Timeframe target: "1m", "5m", "15m", "30m", "1h", "4h"
    
    Returns
    -------
    pd.DataFrame
        DataFrame yang sudah di-resample dengan kolom yang sama.
    """
    df_resample = df.copy()
    
    # Pastikan open_time adalah datetime
    if not pd.api.types.is_datetime64_any_dtype(df_resample["open_time"]):
        df_resample["open_time"] = pd.to_datetime(df_resample["open_time"], errors="coerce", utc=True)
    
    # Set open_time sebagai index untuk resample
    df_resample = df_resample.set_index("open_time")
    
    # Mapping timeframe ke pandas frequency
    timeframe_map = {
        "1m": "1min",
        "5m": "5min",
        "15m": "15min",
        "30m": "30min",
        "1h": "1H",
        "4h": "4H",
    }
    
    if timeframe not in timeframe_map:
        # Jika timeframe tidak dikenal, return asli
        return df_resample.reset_index()
    
    freq = timeframe_map[timeframe]
    
    # Resample OHLCV dengan aturan standar:
    # - open: ambil open pertama
    # - high: ambil high maksimum
    # - low: ambil low minimum
    # - close: ambil close terakhir
    # - volume: jumlahkan semua volume
    df_resampled = df_resample.resample(freq).agg({
        "open": "first",
        "high": "max",
        "low": "min",
        "close": "last",
        "volume": "sum",
    })
    
    # Kolom lain (jika ada) diambil yang terakhir
    kolom_lain = [col for col in df_resample.columns if col not in ["open", "high", "low", "close", "volume"]]
    if kolom_lain:
        for col in kolom_lain:
            if col in df_resample.columns:
                df_resampled[col] = df_resample[col].resample(freq).last()
    
    # Hapus baris yang NaN (karena resample bisa menghasilkan baris kosong)
    df_resampled = df_resampled.dropna(subset=["open", "high", "low", "close"])
    
    # Reset index agar open_time menjadi kolom lagi
    df_resampled = df_resampled.reset_index()
    
    # CRITICAL FIX: Pastikan tidak ada NaT di open_time
    if "open_time" in df_resampled.columns:
        df_resampled = df_resampled.dropna(subset=["open_time"])
        # Convert ke datetime jika belum
        df_resampled["open_time"] = pd.to_datetime(df_resampled["open_time"], errors="coerce")
        # Drop lagi jika masih ada NaT setelah convert
        df_resampled = df_resampled.dropna(subset=["open_time"])
    
    # Pastikan semua kolom numeric tidak ada NaN
    numeric_cols = ["open", "high", "low", "close", "volume"]
    for col in numeric_cols:
        if col in df_resampled.columns:
            df_resampled[col] = df_resampled[col].fillna(method='ffill').fillna(method='bfill').fillna(0)
    
    return df_resampled


def prepare_data_for_mode(df: pd.DataFrame, trading_mode: str) -> pd.DataFrame:
    """
    Siapkan data untuk trading mode tertentu dengan resample dan hitung indikator ulang.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame M1 yang sudah di-preprocess (sudah ada indikator dasar).
    trading_mode : str
        Trading mode: "aktif", "santai", atau "pasif"
    
    Returns
    -------
    pd.DataFrame
        DataFrame yang sudah di-resample dan dihitung indikator ulang sesuai mode.
    """
    # Mapping mode ke timeframe
    mode_timeframe = {
        "aktif": "1h",     # H1 data untuk mode aktif (1-4H)
        "santai": "4h",    # 4H untuk mode santai (4-12H)
        "pasif": "1d",     # Daily untuk mode pasif (12H-3D)
    }
    
    timeframe = mode_timeframe.get(trading_mode, "1m")
    
    # Jika mode aktif, bisa langsung pakai H1 tanpa resample
    if trading_mode == "aktif" and timeframe == "1h":
        # Tidak perlu resample, tapi pastikan indikator sudah dihitung
        if "rsi_6" not in df.columns:
            df = tambah_indikator_ke_df(df)
        return df
    
    # Resample ke timeframe yang sesuai
    df_resampled = resample_ohlcv(df, timeframe)
    
    # Setelah resample, hitung ulang semua indikator
    df_resampled = tambah_indikator_ke_df(df_resampled)
    
    return df_resampled


def ambil_ringkasan_tail(df: pd.DataFrame, jumlah: int = 5) -> List[Dict]:
    """
    Ambil beberapa baris terakhir sebagai contoh respons API.
    """
    contoh = df.tail(jumlah).copy()
    contoh["open_time"] = contoh["open_time"].astype(str)
    return contoh.to_dict(orient="records")


