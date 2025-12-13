"""
Backend Leon Liquidity Engine v3.0
Support untuk Spot & Futures trading dengan AI prediction.
"""

from io import BytesIO
from pathlib import Path
from typing import List, Optional
from datetime import datetime
import shutil

import pandas as pd
from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

# Import dari modules yang sudah di-refactor
from .core.config import UPLOADS_DIR, PROCESSED_DIR, TRADING_MODES
from .models import init_db
from .api import signals_router, binance_router

from .services.praproses_data import (
    simpan_hasil_preprocess,
    tambah_indikator_ke_df,
    PERIODE_RSI_AKTIF,
    PERIODE_RSI_INTRADAY_1,
    PERIODE_RSI_INTRADAY_2,
    PERIODE_RSI_SWING,
    PERIODE_EMA_9,
    PERIODE_EMA_20,
    PERIODE_EMA_50,
    PERIODE_EMA_200,
    PERIODE_ATR,
)
from .services.generator_sinyal_unified import generate_sinyal_dari_folder_honest
from .services.binance_realtime import (
    binance_fetcher,
    SUPPORTED_SYMBOLS,
)
from .services.lstm_predictor import lstm_predictor, get_prediction_for_symbol

# Folder paths (menggunakan config)
FOLDER_DATA_BASE = UPLOADS_DIR
FOLDER_HASIL_BASE = PROCESSED_DIR

# Daftar kolom minimal agar data bisa dipakai untuk analisis OHLCV.
KOLOM_WAJIB: List[str] = ["open_time", "open", "high", "low", "close", "volume"]

# Periode indikator yang FIXED (tidak bisa diubah user)
# Untuk kompatibilitas lama, pakai RSI swing sebagai default.
PERIODE_RSI_DEFAULT = PERIODE_RSI_SWING

# Header standar untuk data Binance Vision (tanpa header)
HEADER_BINANCE_VISION: List[str] = [
    "open_time", "open", "high", "low", "close", "volume",
    "close_time", "quote_volume", "count", "taker_buy_volume",
    "taker_buy_quote_volume", "ignore"
]

aplikasi = FastAPI(
    title="Leon Liquidity Engine API",
    description="Trading Signal Generator dengan AI Prediction untuk Spot & Futures",
    version="3.0.0",
)

# Include routers dari api module
aplikasi.include_router(signals_router)
aplikasi.include_router(binance_router)


@aplikasi.on_event("startup")
async def startup_event():
    """Initialize database saat startup"""
    init_db()
    print("Leon Liquidity Engine v3.0 started!")
    print("Database initialized.")


@aplikasi.get("/cek-kesehatan")
async def cek_kesehatan():
    """
    Endpoint untuk memastikan server hidup.
    Mengembalikan status sederhana.
    """
    return {
        "status": "sehat",
        "version": "3.0.0",
        "features": ["spot", "futures", "signals", "ai_prediction"],
        "timestamp": datetime.now().isoformat()
    }


# ============================================================================
# ENDPOINT MANAJEMEN FOLDER
# ============================================================================

@aplikasi.get("/folder/daftar")
async def daftar_folder():
    """
    Mengembalikan daftar semua folder yang ada di data/uploads.
    """
    if not FOLDER_DATA_BASE.exists():
        return {"folder": []}
    
    daftar_folder = [
        d.name for d in FOLDER_DATA_BASE.iterdir() 
        if d.is_dir() and not d.name.startswith(".")
    ]
    return {"folder": sorted(daftar_folder)}


class PermintaanBuatFolder(BaseModel):
    """Model untuk membuat folder baru."""
    nama_folder: str = Field(..., min_length=1, max_length=100, description="Nama folder baru.")


@aplikasi.post("/folder/buat")
async def buat_folder(perintah: PermintaanBuatFolder):
    """
    Membuat folder baru untuk menyimpan file CSV.
    """
    # Validasi nama folder (hindari karakter berbahaya)
    nama_bersih = perintah.nama_folder.strip()
    if not nama_bersih or "/" in nama_bersih or "\\" in nama_bersih:
        raise HTTPException(status_code=400, detail="Nama folder tidak valid.")
    
    path_folder = FOLDER_DATA_BASE / nama_bersih
    if path_folder.exists():
        raise HTTPException(status_code=400, detail=f"Folder '{nama_bersih}' sudah ada.")
    
    path_folder.mkdir(parents=True, exist_ok=True)
    # Buat juga folder processed untuk folder ini
    (FOLDER_HASIL_BASE / nama_bersih).mkdir(parents=True, exist_ok=True)
    
    return {
        "nama_folder": nama_bersih,
        "pesan": f"Folder '{nama_bersih}' berhasil dibuat.",
        "lokasi": str(path_folder),
    }


class PermintaanRenameFolder(BaseModel):
    """Model untuk rename folder."""
    nama_lama: str = Field(..., description="Nama folder yang akan diubah.")
    nama_baru: str = Field(..., min_length=1, max_length=100, description="Nama folder baru.")


@aplikasi.put("/folder/rename")
async def rename_folder(perintah: PermintaanRenameFolder):
    """
    Mengubah nama folder.
    """
    nama_lama_bersih = perintah.nama_lama.strip()
    nama_baru_bersih = perintah.nama_baru.strip()
    
    if not nama_baru_bersih or "/" in nama_baru_bersih or "\\" in nama_baru_bersih:
        raise HTTPException(status_code=400, detail="Nama folder baru tidak valid.")
    
    path_lama = FOLDER_DATA_BASE / nama_lama_bersih
    path_baru = FOLDER_DATA_BASE / nama_baru_bersih
    
    if not path_lama.exists():
        raise HTTPException(status_code=404, detail=f"Folder '{nama_lama_bersih}' tidak ditemukan.")
    
    if path_baru.exists():
        raise HTTPException(status_code=400, detail=f"Folder '{nama_baru_bersih}' sudah ada.")
    
    # Rename folder uploads
    path_lama.rename(path_baru)
    # Rename folder processed juga
    path_lama_processed = FOLDER_HASIL_BASE / nama_lama_bersih
    path_baru_processed = FOLDER_HASIL_BASE / nama_baru_bersih
    if path_lama_processed.exists():
        path_lama_processed.rename(path_baru_processed)
    
    return {
        "nama_lama": nama_lama_bersih,
        "nama_baru": nama_baru_bersih,
        "pesan": f"Folder '{nama_lama_bersih}' berhasil diubah menjadi '{nama_baru_bersih}'.",
    }


@aplikasi.delete("/folder/hapus")
async def hapus_folder(nama_folder: str = Query(..., description="Nama folder yang akan dihapus.")):
    """
    Menghapus folder beserta semua isinya.
    """
    nama_bersih = nama_folder.strip()
    path_folder = FOLDER_DATA_BASE / nama_bersih
    
    if not path_folder.exists():
        raise HTTPException(status_code=404, detail=f"Folder '{nama_bersih}' tidak ditemukan.")
    
    # Hapus folder uploads
    shutil.rmtree(path_folder)
    # Hapus folder processed juga
    path_folder_processed = FOLDER_HASIL_BASE / nama_bersih
    if path_folder_processed.exists():
        shutil.rmtree(path_folder_processed)
    
    return {
        "nama_folder": nama_bersih,
        "pesan": f"Folder '{nama_bersih}' beserta isinya berhasil dihapus.",
    }


@aplikasi.get("/", response_class=HTMLResponse)
async def halaman_utama():
    """
    Halaman dashboard sederhana berbasis HTML/JS.
    Menggunakan tema gelap dengan sidebar dan aksen neon.
    File HTML sekarang dipisahkan ke frontend/index.html untuk kemudahan maintenance.
    """
    # Path relatif dari root project (dimana uvicorn dijalankan)
    path_html = Path("frontend") / "index.html"
    if not path_html.exists():
        raise HTTPException(status_code=500, detail="File frontend/index.html tidak ditemukan.")
    return FileResponse(path_html, media_type="text/html")


def _normalisasi_csv_binance(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalisasi CSV dari Binance Vision yang mungkin tidak punya header.
    Auto-detect dan assign header jika diperlukan.
    
    Format Binance Vision (tanpa header):
    open_time,open,high,low,close,volume,close_time,quote_volume,count,taker_buy_volume,taker_buy_quote_volume,ignore
    """
    # Cek apakah kolom pertama adalah angka (kemungkinan open_time dalam format timestamp)
    # Jika iya, berarti CSV tidak punya header
    if len(df.columns) == len(HEADER_BINANCE_VISION):
        kolom_pertama = df.columns[0]
        # Cek apakah kolom pertama adalah angka (timestamp) atau string yang mirip header
        try:
            # Coba convert kolom pertama ke float/int
            pd.to_numeric(df.iloc[0, 0], errors='raise')
            # Jika berhasil, berarti ini data tanpa header
            # Assign header sesuai format Binance Vision
            df.columns = HEADER_BINANCE_VISION
        except (ValueError, TypeError):
            # Kolom pertama bukan angka, kemungkinan sudah ada header
            # Tapi cek apakah header sesuai dengan format Binance
            if kolom_pertama.lower() not in ['open_time', 'open', 'high', 'low', 'close', 'volume']:
                # Header tidak sesuai, coba assign ulang
                df.columns = HEADER_BINANCE_VISION[:len(df.columns)]
    
    return df


def _pastikan_kolom_wajib(df: pd.DataFrame) -> None:
    """
    Pastikan kolom wajib tersedia di DataFrame.
    """
    kolom_tidak_ada = [kol for kol in KOLOM_WAJIB if kol not in df.columns]
    if kolom_tidak_ada:
        raise HTTPException(
            status_code=400,
            detail=f"Kolom wajib hilang: {', '.join(kolom_tidak_ada)}. Format CSV harus sesuai Binance: {', '.join(HEADER_BINANCE_VISION)}",
        )


def _konversi_waktu(series_waktu: pd.Series) -> pd.Series:
    """
    Konversi kolom open_time ke datetime.
    Otomatis mendeteksi apakah nilai berupa detik atau milidetik.
    """
    # Coba asumsikan milidetik (umum di Binance)
    waktu_dt = pd.to_datetime(series_waktu, unit="ms", errors="coerce")
    if waktu_dt.isna().all():
        # Jika gagal semua, coba parse otomatis (string ISO atau detik)
        waktu_dt = pd.to_datetime(series_waktu, errors="coerce", utc=True)
    return waktu_dt


@aplikasi.post("/unggah-csv/")
async def unggah_csv(
    berkas: UploadFile = File(...),
    folder: str = Query(..., description="Nama folder tujuan untuk menyimpan file.")
):
    """
    Endpoint untuk menerima berkas CSV dari pengguna.
    Data disimpan ke folder `data/uploads/<folder>/` dan dikembalikan ringkasan statistiknya.
    """
    if not berkas.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Hanya berkas CSV yang diizinkan.")

    # Validasi nama folder
    nama_folder_bersih = folder.strip()
    if not nama_folder_bersih or "/" in nama_folder_bersih or "\\" in nama_folder_bersih:
        raise HTTPException(status_code=400, detail="Nama folder tidak valid.")
    
    # Pastikan folder ada
    path_folder = FOLDER_DATA_BASE / nama_folder_bersih
    if not path_folder.exists():
        raise HTTPException(status_code=404, detail=f"Folder '{nama_folder_bersih}' tidak ditemukan. Buat folder terlebih dahulu.")

    isi_berkas = await berkas.read()
    if not isi_berkas:
        raise HTTPException(status_code=400, detail="Berkas kosong.")

    try:
        # Baca CSV, coba dengan header dulu
        df = pd.read_csv(BytesIO(isi_berkas))
        # Normalisasi untuk handle CSV tanpa header (format Binance Vision)
        df = _normalisasi_csv_binance(df)
    except Exception as err:  # pragma: no cover - FastAPI run-time
        raise HTTPException(status_code=400, detail=f"Gagal membaca CSV: {err}") from err

    _pastikan_kolom_wajib(df)

    df["open_time"] = _konversi_waktu(df["open_time"])
    if df["open_time"].isna().all():
        raise HTTPException(
            status_code=400,
            detail="Kolom open_time tidak bisa dikonversi ke datetime.",
        )

    jumlah_baris = len(df)
    waktu_mulai = df["open_time"].min()
    waktu_selesai = df["open_time"].max()

    # Simpan berkas asli ke folder yang dipilih
    path_simpan = path_folder / berkas.filename
    with open(path_simpan, "wb") as tujuan:
        tujuan.write(isi_berkas)

    return {
        "nama_berkas": berkas.filename,
        "folder": nama_folder_bersih,
        "jumlah_baris": jumlah_baris,
        "kolom": list(df.columns),
        "waktu_mulai": waktu_mulai.isoformat(),
        "waktu_selesai": waktu_selesai.isoformat(),
        "lokasi_simpan": str(path_simpan),
        "pesan": f"Berkas CSV berhasil disimpan ke folder '{nama_folder_bersih}'.",
    }


class PermintaanPraProsesSemua(BaseModel):
    """
    Model request body untuk proses indikator dasar (semua file di folder tertentu).
    Periode indikator sudah FIXED: RSI 14, EMA 50, EMA 200.
    """

    folder: str = Field(..., description="Nama folder yang akan diproses.")


@aplikasi.post("/pra-proses/indikator/")
async def pra_proses_indikator(perintah: PermintaanPraProsesSemua):
    """
    Proses semua berkas CSV di folder uploads/<folder> dan tambahkan indikator RSI & EMA.
    Hasil disimpan ke data/processed/<folder>/.
    """
    nama_folder_bersih = perintah.folder.strip()
    path_folder = FOLDER_DATA_BASE / nama_folder_bersih
    
    if not path_folder.exists():
        raise HTTPException(status_code=404, detail=f"Folder '{nama_folder_bersih}' tidak ditemukan.")

    daftar = sorted(path_folder.glob("*.csv"))
    if not daftar:
        raise HTTPException(
            status_code=404,
            detail=f"Belum ada berkas CSV di folder '{nama_folder_bersih}'.",
        )

    # Pastikan folder processed ada
    path_folder_processed = FOLDER_HASIL_BASE / nama_folder_bersih
    path_folder_processed.mkdir(parents=True, exist_ok=True)

    hasil_ringkas = []

    for path_sumber in daftar:
        try:
            df = pd.read_csv(path_sumber)
            # Normalisasi untuk handle CSV tanpa header
            df = _normalisasi_csv_binance(df)
            _pastikan_kolom_wajib(df)
            
            # Pastikan open_time adalah datetime dengan benar
            df["open_time"] = _konversi_waktu(df["open_time"])
            if df["open_time"].isna().all():
                raise ValueError("open_time tidak valid")
            
            # Pastikan close_time adalah integer (timestamp milidetik) jika ada
            if "close_time" in df.columns:
                try:
                    df["close_time"] = pd.to_numeric(df["close_time"], errors="coerce").fillna(0).astype(int)
                except:
                    pass

            # Gunakan periode FIXED (RSI 6/8/10/14, EMA 9/20/50/200, ATR 14)
            df_indikator = tambah_indikator_ke_df(df)
            path_hasil = simpan_hasil_preprocess(
                df_indikator, path_sumber.name, path_folder_processed
            )

            hasil_ringkas.append(
                {
                    "nama_berkas": path_sumber.name,
                    "jumlah_baris": len(df_indikator),
                    "lokasi_hasil": str(path_hasil),
                }
            )
        except Exception as err:  # pragma: no cover
            hasil_ringkas.append(
                {
                    "nama_berkas": path_sumber.name,
                    "error": str(err),
                }
            )

    return {
        "folder": nama_folder_bersih,
        "periode_rsi": {
            "aktif": PERIODE_RSI_AKTIF,
            "santai_1": PERIODE_RSI_INTRADAY_1,
            "santai_2": PERIODE_RSI_INTRADAY_2,
            "pasif": PERIODE_RSI_SWING,
        },
        "periode_ema": {
            "ema_9": PERIODE_EMA_9,
            "ema_20": PERIODE_EMA_20,
            "ema_50": PERIODE_EMA_50,
            "ema_200": PERIODE_EMA_200,
        },
        "periode_atr": PERIODE_ATR,
        "jumlah_berkas": len(daftar),
        "ringkasan": hasil_ringkas,
    }


@aplikasi.delete("/unggah-csv/hapus")
async def hapus_file(
    nama_berkas: str = Query(..., description="Nama file yang akan dihapus."),
    folder: str = Query(..., description="Nama folder tempat file berada.")
):
    """
    Menghapus file CSV dari folder uploads/<folder>/.
    """
    nama_folder_bersih = folder.strip()
    path_folder = FOLDER_DATA_BASE / nama_folder_bersih
    
    if not path_folder.exists():
        raise HTTPException(status_code=404, detail=f"Folder '{nama_folder_bersih}' tidak ditemukan.")
    
    path_file = path_folder / nama_berkas
    if not path_file.exists():
        raise HTTPException(status_code=404, detail=f"File '{nama_berkas}' tidak ditemukan di folder '{nama_folder_bersih}'.")
    
    path_file.unlink()
    
    return {
        "nama_berkas": nama_berkas,
        "folder": nama_folder_bersih,
        "pesan": f"File '{nama_berkas}' berhasil dihapus dari folder '{nama_folder_bersih}'.",
    }


@aplikasi.get("/unggah-csv/daftar")
async def daftar_berkas_unggahan(
    folder: str = Query(..., description="Nama folder yang akan dilihat daftar filenya.")
):
    """
    Mengembalikan daftar berkas CSV yang tersedia di folder uploads/<folder>.
    """
    nama_folder_bersih = folder.strip()
    path_folder = FOLDER_DATA_BASE / nama_folder_bersih
    
    if not path_folder.exists():
        raise HTTPException(status_code=404, detail=f"Folder '{nama_folder_bersih}' tidak ditemukan.")
    
    daftar = sorted(path_folder.glob("*.csv"))
    return {
        "folder": nama_folder_bersih,
        "jumlah": len(daftar),
        "berkas": [path.name for path in daftar],
    }


@aplikasi.get("/processed-csv/daftar")
async def daftar_berkas_processed(
    folder: str = Query(..., description="Nama folder yang akan dilihat daftar file processed-nya.")
):
    """
    Mengembalikan daftar berkas CSV processed yang tersedia di folder processed/<folder>.
    """
    nama_folder_bersih = folder.strip()
    path_folder = FOLDER_HASIL_BASE / nama_folder_bersih
    
    if not path_folder.exists():
        return {
            "folder": nama_folder_bersih,
            "jumlah": 0,
            "berkas": [],
        }
    
    daftar = sorted(path_folder.glob("*.csv"))
    return {
        "folder": nama_folder_bersih,
        "jumlah": len(daftar),
        "berkas": [path.name for path in daftar],
    }


@aplikasi.get("/unggah-csv/preview")
async def preview_berkas(
    nama_berkas: str,
    folder: str = Query(..., description="Nama folder tempat file berada."),
    jenis: str = "processed",
    limit: int = 10,
):
    """
    Mengambil beberapa baris contoh dari berkas tertentu agar bisa dilihat di UI.

    - `jenis='processed'`  -> ambil dari folder data/processed/<folder>/ jika ada, kalau tidak fallback ke uploads
    - `jenis='upload'`     -> paksa ambil dari uploads/<folder>/
    """
    nama_folder_bersih = folder.strip()
    path_folder_upload = FOLDER_DATA_BASE / nama_folder_bersih
    path_folder_processed = FOLDER_HASIL_BASE / nama_folder_bersih
    
    if not path_folder_upload.exists():
        raise HTTPException(status_code=404, detail=f"Folder '{nama_folder_bersih}' tidak ditemukan.")

    if jenis not in {"processed", "upload"}:
        raise HTTPException(status_code=400, detail="Parameter 'jenis' harus 'processed' atau 'upload'.")

    path_upload = path_folder_upload / nama_berkas
    path_processed = path_folder_processed / (Path(nama_berkas).with_suffix(".processed.csv").name)

    path_sumber = None
    sumber = ""

    if jenis == "upload":
        path_sumber = path_upload
        sumber = "upload"
    else:
        if path_processed.exists():
            path_sumber = path_processed
            sumber = "processed"
        else:
            path_sumber = path_upload
            sumber = "upload"

    if not path_sumber.exists():
        raise HTTPException(status_code=404, detail="Berkas tidak ditemukan di uploads maupun processed.")

    try:
        df = pd.read_csv(path_sumber)
    except Exception as err:  # pragma: no cover
        raise HTTPException(status_code=400, detail=f"Gagal membaca CSV: {err}") from err

    if "open_time" in df.columns:
        df["open_time"] = pd.to_datetime(df["open_time"], errors="coerce")

    total_baris = len(df)
    contoh = df.head(limit).copy()
    if "open_time" in contoh.columns:
        contoh["open_time"] = contoh["open_time"].astype(str)

    ringkasan = {}
    if "open_time" in df.columns:
        ringkasan["waktu_mulai"] = str(df["open_time"].min())
        ringkasan["waktu_selesai"] = str(df["open_time"].max())
    if "close" in df.columns:
        ringkasan["close_min"] = float(df["close"].min())
        ringkasan["close_max"] = float(df["close"].max())
    if "volume" in df.columns:
        ringkasan["volume_total"] = float(df["volume"].sum())

    return {
        "nama_berkas": nama_berkas,
        "sumber": sumber,
        "jumlah_baris": total_baris,
        "kolom": list(df.columns),
        "contoh": contoh.to_dict(orient="records"),
        "ringkasan": ringkasan,
    }


# ============================================================================
# ENDPOINT SINYAL TRADING
# ============================================================================

class PermintaanGenerateSinyal(BaseModel):
    """Model request body untuk generate sinyal trading."""
    folder: str = Field(..., description="Nama folder yang akan dianalisis.")
    mode_trading: str = Field("santai", description="Mode trading: 'aktif', 'santai', atau 'pasif' (default: 'santai').")
    rsi_oversold: Optional[float] = Field(None, ge=0, le=50, description="Override RSI oversold (jika None, pakai dari mode trading).")
    rsi_overbought: Optional[float] = Field(None, ge=50, le=100, description="Override RSI overbought (jika None, pakai dari mode trading).")
    rasio_risk_reward: Optional[float] = Field(None, ge=0.5, le=10.0, description="Override rasio RR (jika None, pakai dari mode trading).")
    confidence_minimum: float = Field(0.50, ge=0.0, le=1.0, description="Confidence minimum untuk generate sinyal (default: 0.50 = 50%). Range: 0.0-1.0")
    # Removed gunakan_delta - now using unified honest system only


@aplikasi.post("/sinyal/generate")
async def generate_sinyal(perintah: PermintaanGenerateSinyal):
    """
    Generate sinyal trading untuk semua file processed di folder tertentu.
    
    SISTEM DELTA:
    - Akurasi tinggi (target 70-80% winrate)
    - Confluence fleksibel (3/6 vs 4/6)
    - Scoring confidence advanced (50-95%)
    - Filter confidence minimum
    - Divergence opsional (bonus confidence)
    - S/R requirements realistis (<2%)
    
    Returns: Sinyal dengan confidence >= confidence_minimum
    """
    nama_folder_bersih = perintah.folder.strip()
    path_folder_processed = FOLDER_HASIL_BASE / nama_folder_bersih
    
    if not path_folder_processed.exists():
        raise HTTPException(status_code=404, detail=f"Folder processed '{nama_folder_bersih}' tidak ditemukan. Jalankan pra-proses indikator terlebih dahulu.")

    try:
        # Confidence minimum EXPERT LEVEL untuk kejujuran semua mode
        confidence_min = max(perintah.confidence_minimum, 0.60)  # Minimum 60% untuk expert mode
        
        # Gunakan sistem UNIFIED HONEST
        daftar_sinyal = generate_sinyal_dari_folder_honest(
            str(path_folder_processed),
            pair="",
            mode_trading=perintah.mode_trading,
            confidence_minimum=confidence_min,
            rsi_oversold=perintah.rsi_oversold,
            rsi_overbought=perintah.rsi_overbought,
            rasio_risk_reward=perintah.rasio_risk_reward,
        )
        versi_sistem = "UNIFIED HONEST (Kejujuran & Akurasi)"
        
        # Hitung statistik confidence
        if daftar_sinyal:
            confidences = [s["confidence"] for s in daftar_sinyal]
            rata_rata_confidence = sum(confidences) / len(confidences)
            confidence_terendah = min(confidences)
            confidence_tertinggi = max(confidences)
            
            # Hitung berdasarkan range confidence
            jumlah_confidence_tinggi = len([c for c in confidences if c >= 0.70])
            jumlah_confidence_sedang = len([c for c in confidences if 0.60 <= c < 0.70])
            jumlah_confidence_rendah = len([c for c in confidences if c < 0.60])
            
            # BACKTEST STATISTICS - REAL PERFORMANCE
            backtest_results = [s.get("backtest_result", "UNKNOWN") for s in daftar_sinyal]
            pnl_values = [s.get("pnl_percent", 0) for s in daftar_sinyal if s.get("backtest_result") in ["HIT_TP", "HIT_SL"]]
            duration_values = [s.get("duration_hours", 0) for s in daftar_sinyal if s.get("backtest_result") in ["HIT_TP", "HIT_SL"]]
            
            # Win/Loss counts
            hit_tp_count = backtest_results.count("HIT_TP")
            hit_sl_count = backtest_results.count("HIT_SL")
            timeout_count = backtest_results.count("TIMEOUT")
            total_closed = hit_tp_count + hit_sl_count
            
            # Calculate statistics
            win_rate = (hit_tp_count / total_closed * 100) if total_closed > 0 else 0
            avg_pnl = sum(pnl_values) / len(pnl_values) if pnl_values else 0
            avg_duration = sum(duration_values) / len(duration_values) if duration_values else 0
            
            # Profit/Loss breakdown
            profitable_trades = [pnl for pnl in pnl_values if pnl > 0]
            losing_trades = [pnl for pnl in pnl_values if pnl < 0]
            avg_profit = sum(profitable_trades) / len(profitable_trades) if profitable_trades else 0
            avg_loss = sum(losing_trades) / len(losing_trades) if losing_trades else 0
            
            backtest_stats = {
                "total_signals": len(daftar_sinyal),
                "hit_tp": hit_tp_count,
                "hit_sl": hit_sl_count,
                "timeout": timeout_count,
                "win_rate": round(win_rate, 1),
                "avg_pnl": round(avg_pnl, 2),
                "avg_duration_hours": round(avg_duration, 1),
                "avg_profit": round(avg_profit, 2),
                "avg_loss": round(avg_loss, 2),
                "total_closed": total_closed
            }
        else:
            rata_rata_confidence = 0
            confidence_terendah = 0
            confidence_tertinggi = 0
            jumlah_confidence_tinggi = 0
            jumlah_confidence_sedang = 0
            jumlah_confidence_rendah = 0
            backtest_stats = {
                "total_signals": 0,
                "hit_tp": 0,
                "hit_sl": 0,
                "timeout": 0,
                "win_rate": 0,
                "avg_pnl": 0,
                "avg_duration_hours": 0,
                "avg_profit": 0,
                "avg_loss": 0,
                "total_closed": 0
            }
        
        return {
            "folder": nama_folder_bersih,
            "sistem": versi_sistem,
            "jumlah_sinyal": len(daftar_sinyal),
            "parameter": {
                "mode_trading": perintah.mode_trading,
                "rsi_oversold": perintah.rsi_oversold,
                "rsi_overbought": perintah.rsi_overbought,
                "rasio_risk_reward": perintah.rasio_risk_reward,
                "confidence_minimum": perintah.confidence_minimum,
            },
            "statistik_confidence": {
                "rata_rata": round(rata_rata_confidence, 4),
                "terendah": round(confidence_terendah, 4),
                "tertinggi": round(confidence_tertinggi, 4),
                "jumlah_tinggi": jumlah_confidence_tinggi,  # >= 70%
                "jumlah_sedang": jumlah_confidence_sedang,  # 60-70%
                "jumlah_rendah": jumlah_confidence_rendah,  # < 60%
            },
            "backtest_statistics": backtest_stats,  # REAL PERFORMANCE DATA
            "sinyal": daftar_sinyal,
        }
    except Exception as err:  # pragma: no cover
        raise HTTPException(status_code=500, detail=f"Gagal generate sinyal: {err}") from err


# ============================================================================
# ENDPOINT BINANCE REAL-TIME DATA
# ============================================================================

@aplikasi.get("/binance/symbols")
async def daftar_symbols():
    """
    Mengembalikan daftar symbols yang didukung untuk real-time data.
    """
    return {
        "symbols": SUPPORTED_SYMBOLS,
        "jumlah": len(SUPPORTED_SYMBOLS),
        "pesan": "Symbols yang didukung untuk real-time data dari Binance."
    }


@aplikasi.get("/binance/price/{symbol}")
async def harga_terkini(symbol: str):
    """
    Ambil harga terkini untuk symbol tertentu dari Binance.
    
    Parameters:
    -----------
    symbol: str - Trading pair (e.g., "BTCUSDT")
    """
    try:
        data = await binance_fetcher.get_ticker_price(symbol.upper())
        return {
            "status": "sukses",
            "data": data
        }
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Gagal mengambil harga: {err}")


@aplikasi.get("/binance/prices")
async def semua_harga():
    """
    Ambil harga terkini untuk semua symbols yang didukung.
    """
    try:
        data = await binance_fetcher.get_multiple_tickers(SUPPORTED_SYMBOLS)
        return {
            "status": "sukses",
            "jumlah": len(data),
            "data": data
        }
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Gagal mengambil harga: {err}")


@aplikasi.get("/binance/ticker24h/{symbol}")
async def statistik_24h(symbol: str):
    """
    Ambil statistik 24 jam untuk symbol tertentu.
    
    Parameters:
    -----------
    symbol: str - Trading pair (e.g., "BTCUSDT")
    """
    try:
        data = await binance_fetcher.get_24h_ticker(symbol.upper())
        return {
            "status": "sukses",
            "data": data
        }
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Gagal mengambil statistik 24h: {err}")


@aplikasi.get("/binance/klines/{symbol}")
async def ambil_klines(
    symbol: str,
    interval: str = Query("1h", description="Interval: 1m, 5m, 15m, 1h, 4h, 1d"),
    limit: int = Query(100, ge=1, le=1000, description="Jumlah candle (max 1000)")
):
    """
    Ambil data klines (candlestick) dari Binance.
    
    Parameters:
    -----------
    symbol: str - Trading pair (e.g., "BTCUSDT")
    interval: str - Timeframe ("1m", "5m", "15m", "1h", "4h", "1d")
    limit: int - Jumlah candle (max 1000)
    """
    valid_intervals = ["1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h", "1d", "3d", "1w", "1M"]
    if interval not in valid_intervals:
        raise HTTPException(status_code=400, detail=f"Interval tidak valid. Pilih dari: {valid_intervals}")
    
    try:
        data = await binance_fetcher.get_klines(symbol.upper(), interval, limit)
        return {
            "status": "sukses",
            "symbol": symbol.upper(),
            "interval": interval,
            "jumlah": len(data),
            "data": data
        }
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Gagal mengambil klines: {err}")


@aplikasi.post("/binance/analyze/{symbol}")
async def analisis_realtime(
    symbol: str,
    mode_trading: str = Query("santai", description="Mode: aktif, santai, pasif"),
    interval: str = Query("1h", description="Interval: 1h, 4h"),
    limit: int = Query(100, ge=50, le=500, description="Jumlah candle untuk analisis")
):
    """
    Analisis real-time: Ambil data dari Binance, proses indikator, dan generate sinyal.
    
    Parameters:
    -----------
    symbol: str - Trading pair (e.g., "BTCUSDT")
    mode_trading: str - Mode trading (aktif, santai, pasif)
    interval: str - Timeframe untuk analisis
    limit: int - Jumlah candle untuk analisis
    """
    from .services.praproses_data import tambah_indikator_ke_df
    from .services.generator_sinyal_unified import scan_sinyal_honest, TRADING_STYLES
    
    if mode_trading not in TRADING_STYLES:
        raise HTTPException(status_code=400, detail=f"Mode trading tidak valid. Pilih dari: {list(TRADING_STYLES.keys())}")
    
    try:
        # 1. Ambil data dari Binance
        klines = await binance_fetcher.get_klines(symbol.upper(), interval, limit)
        
        if not klines:
            raise HTTPException(status_code=404, detail="Tidak ada data dari Binance")
        
        # 2. Convert ke DataFrame
        df = pd.DataFrame(klines)
        df['open_time'] = pd.to_datetime(df['open_time'], unit='ms')
        
        # 3. Tambah indikator
        df_dengan_indikator = tambah_indikator_ke_df(df)
        
        # 4. Generate sinyal
        sinyal_list = scan_sinyal_honest(
            df=df_dengan_indikator,
            pair=symbol.upper(),
            mode_trading=mode_trading,
            confidence_minimum=0.60
        )
        
        # 5. Ambil harga terkini
        harga_terkini = await binance_fetcher.get_ticker_price(symbol.upper())
        
        return {
            "status": "sukses",
            "symbol": symbol.upper(),
            "mode_trading": mode_trading,
            "interval": interval,
            "harga_terkini": harga_terkini["price"],
            "jumlah_candle": len(df_dengan_indikator),
            "jumlah_sinyal": len(sinyal_list),
            "sinyal": sinyal_list[-5:] if sinyal_list else [],  # 5 sinyal terbaru
            "indikator_terkini": {
                "rsi_6": round(df_dengan_indikator['rsi_6'].iloc[-1], 2) if 'rsi_6' in df_dengan_indikator.columns else None,
                "rsi_14": round(df_dengan_indikator['rsi_14'].iloc[-1], 2) if 'rsi_14' in df_dengan_indikator.columns else None,
                "ema_9": round(df_dengan_indikator['ema_9'].iloc[-1], 2) if 'ema_9' in df_dengan_indikator.columns else None,
                "ema_20": round(df_dengan_indikator['ema_20'].iloc[-1], 2) if 'ema_20' in df_dengan_indikator.columns else None,
                "ema_50": round(df_dengan_indikator['ema_50'].iloc[-1], 2) if 'ema_50' in df_dengan_indikator.columns else None,
                "ema_200": round(df_dengan_indikator['ema_200'].iloc[-1], 2) if 'ema_200' in df_dengan_indikator.columns else None,
            },
            "timestamp": harga_terkini["timestamp"]
        }
        
    except HTTPException:
        raise
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Gagal analisis real-time: {err}")


# ============================================================================
# ENDPOINT LSTM PREDICTION
# ============================================================================

@aplikasi.get("/lstm/predict/{symbol}")
async def prediksi_lstm(
    symbol: str,
    interval: str = Query("1h", description="Interval: 1h, 4h"),
    limit: int = Query(100, ge=50, le=500, description="Jumlah candle untuk analisis")
):
    """
    Prediksi arah harga menggunakan LSTM atau simulasi.
    
    Parameters:
    -----------
    symbol: str - Trading pair (e.g., "BTCUSDT")
    interval: str - Timeframe untuk analisis
    limit: int - Jumlah candle untuk analisis
    """
    from .services.praproses_data import tambah_indikator_ke_df
    
    try:
        # 1. Ambil data dari Binance
        klines = await binance_fetcher.get_klines(symbol.upper(), interval, limit)
        
        if not klines:
            raise HTTPException(status_code=404, detail="Tidak ada data dari Binance")
        
        # 2. Convert ke DataFrame
        df = pd.DataFrame(klines)
        df['open_time'] = pd.to_datetime(df['open_time'], unit='ms')
        
        # 3. Tambah indikator
        df_dengan_indikator = tambah_indikator_ke_df(df)
        
        # 4. Get prediction
        prediction = get_prediction_for_symbol(df_dengan_indikator, symbol.upper())
        
        # 5. Ambil harga terkini
        harga_terkini = await binance_fetcher.get_ticker_price(symbol.upper())
        
        return {
            "status": "sukses",
            "symbol": symbol.upper(),
            "interval": interval,
            "harga_terkini": harga_terkini["price"],
            "prediksi": prediction,
            "rekomendasi": _generate_recommendation(prediction),
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Gagal prediksi LSTM: {err}")


def _generate_recommendation(prediction: dict) -> dict:
    """Generate trading recommendation berdasarkan prediksi."""
    direction = prediction.get("direction", "NEUTRAL")
    confidence = prediction.get("confidence", 0.5)
    
    if direction == "UP" and confidence >= 0.7:
        return {
            "aksi": "BELI",
            "kekuatan": "KUAT",
            "alasan": f"Prediksi NAIK dengan confidence {confidence*100:.1f}%"
        }
    elif direction == "UP" and confidence >= 0.6:
        return {
            "aksi": "BELI",
            "kekuatan": "SEDANG",
            "alasan": f"Prediksi NAIK dengan confidence {confidence*100:.1f}%"
        }
    elif direction == "DOWN" and confidence >= 0.7:
        return {
            "aksi": "JUAL",
            "kekuatan": "KUAT",
            "alasan": f"Prediksi TURUN dengan confidence {confidence*100:.1f}%"
        }
    elif direction == "DOWN" and confidence >= 0.6:
        return {
            "aksi": "JUAL",
            "kekuatan": "SEDANG",
            "alasan": f"Prediksi TURUN dengan confidence {confidence*100:.1f}%"
        }
    else:
        return {
            "aksi": "TUNGGU",
            "kekuatan": "LEMAH",
            "alasan": f"Sinyal tidak cukup kuat (confidence {confidence*100:.1f}%)"
        }


# Import datetime untuk timestamp
from datetime import datetime


# ============================================================================
# ENDPOINT HYBRID SIGNAL (TECHNICAL + LSTM)
# ============================================================================

@aplikasi.post("/hybrid/analyze/{symbol}")
async def analisis_hybrid(
    symbol: str,
    mode_trading: str = Query("santai", description="Mode: aktif, santai, pasif"),
    interval: str = Query("1h", description="Interval: 1h, 4h"),
    limit: int = Query(100, ge=50, le=500, description="Jumlah candle untuk analisis")
):
    """
    HYBRID SIGNAL: Gabungan analisis Technical Indicators + LSTM AI Prediction.
    
    Sistem ini menggabungkan:
    1. Technical Analysis (RSI, EMA, ATR, S/R, Divergence)
    2. LSTM Deep Learning Prediction
    
    Confidence dihitung dari kombinasi keduanya untuk sinyal yang lebih akurat.
    
    Parameters:
    -----------
    symbol: str - Trading pair (e.g., "BTCUSDT")
    mode_trading: str - Mode trading (aktif, santai, pasif)
    interval: str - Timeframe untuk analisis
    limit: int - Jumlah candle untuk analisis
    """
    from .services.praproses_data import tambah_indikator_ke_df
    from .services.generator_sinyal_unified import scan_sinyal_honest, TRADING_STYLES
    
    if mode_trading not in TRADING_STYLES:
        raise HTTPException(status_code=400, detail=f"Mode trading tidak valid. Pilih dari: {list(TRADING_STYLES.keys())}")
    
    try:
        # 1. Ambil data dari Binance
        klines = await binance_fetcher.get_klines(symbol.upper(), interval, limit)
        
        if not klines:
            raise HTTPException(status_code=404, detail="Tidak ada data dari Binance")
        
        # 2. Convert ke DataFrame
        df = pd.DataFrame(klines)
        df['open_time'] = pd.to_datetime(df['open_time'], unit='ms')
        
        # 3. Tambah indikator
        df_dengan_indikator = tambah_indikator_ke_df(df)
        
        # 4. Get Technical Signal
        sinyal_teknikal = scan_sinyal_honest(
            df=df_dengan_indikator,
            pair=symbol.upper(),
            mode_trading=mode_trading,
            confidence_minimum=0.50  # Lower threshold untuk hybrid
        )
        
        # 5. Get LSTM Prediction
        lstm_prediction = get_prediction_for_symbol(df_dengan_indikator, symbol.upper())
        
        # 6. Ambil harga terkini
        harga_terkini = await binance_fetcher.get_ticker_price(symbol.upper())
        current_price = float(harga_terkini["price"])
        
        # 7. HYBRID ANALYSIS - Gabungkan Technical + LSTM
        hybrid_signals = []
        
        # Ambil sinyal teknikal terbaru (jika ada)
        latest_technical = sinyal_teknikal[-1] if sinyal_teknikal else None
        
        # Analisis LSTM
        lstm_direction = lstm_prediction.get("direction", "NEUTRAL")
        lstm_confidence = lstm_prediction.get("confidence", 0.5)
        
        # Hitung HYBRID CONFIDENCE
        if latest_technical:
            tech_confidence = latest_technical.get("confidence", 0.5)
            tech_type = latest_technical.get("tipe", "NEUTRAL")
            
            # Cek apakah Technical dan LSTM sejalan
            tech_direction = "UP" if tech_type == "BELI" else "DOWN" if tech_type == "JUAL" else "NEUTRAL"
            
            if tech_direction == lstm_direction:
                # CONFLUENCE! Technical dan LSTM sejalan
                # Hybrid confidence = weighted average + bonus
                hybrid_confidence = (tech_confidence * 0.5) + (lstm_confidence * 0.5) + 0.10
                hybrid_confidence = min(0.95, hybrid_confidence)  # Cap at 95%
                confluence_status = "STRONG"
                confluence_bonus = 0.10
            else:
                # DIVERGENCE - Technical dan LSTM berbeda
                # Ambil yang lebih kuat, tapi kurangi confidence
                if tech_confidence > lstm_confidence:
                    hybrid_confidence = tech_confidence * 0.8
                    dominant = "TECHNICAL"
                else:
                    hybrid_confidence = lstm_confidence * 0.8
                    dominant = "LSTM"
                confluence_status = "WEAK"
                confluence_bonus = -0.10
            
            # Generate hybrid signal
            if hybrid_confidence >= 0.60:
                # Tentukan arah berdasarkan confluence
                if confluence_status == "STRONG":
                    final_direction = tech_direction
                else:
                    final_direction = tech_direction if tech_confidence > lstm_confidence else lstm_direction
                
                final_type = "BELI" if final_direction == "UP" else "JUAL"
                
                # Calculate SL/TP dari technical signal
                entry = current_price
                atr = df_dengan_indikator['atr_14'].iloc[-1] if 'atr_14' in df_dengan_indikator.columns else current_price * 0.02
                
                if final_type == "BELI":
                    stop_loss = entry - (atr * 1.5)
                    take_profit = entry + (atr * 3.0)
                else:
                    stop_loss = entry + (atr * 1.5)
                    take_profit = entry - (atr * 3.0)
                
                hybrid_signal = {
                    "tipe": final_type,
                    "entry": round(entry, 2),
                    "stop_loss": round(stop_loss, 2),
                    "take_profit": round(take_profit, 2),
                    "confidence": round(hybrid_confidence, 4),
                    "confluence_status": confluence_status,
                    "technical_signal": tech_type,
                    "technical_confidence": round(tech_confidence, 4),
                    "lstm_direction": lstm_direction,
                    "lstm_confidence": round(lstm_confidence, 4),
                    "alasan": f"[HYBRID {confluence_status}] Technical: {tech_type} ({tech_confidence*100:.0f}%), LSTM: {lstm_direction} ({lstm_confidence*100:.0f}%)",
                    "timestamp": datetime.now().isoformat()
                }
                hybrid_signals.append(hybrid_signal)
        
        else:
            # Tidak ada sinyal teknikal, gunakan LSTM saja
            if lstm_confidence >= 0.65:
                final_type = "BELI" if lstm_direction == "UP" else "JUAL" if lstm_direction == "DOWN" else None
                
                if final_type:
                    entry = current_price
                    atr = df_dengan_indikator['atr_14'].iloc[-1] if 'atr_14' in df_dengan_indikator.columns else current_price * 0.02
                    
                    if final_type == "BELI":
                        stop_loss = entry - (atr * 1.5)
                        take_profit = entry + (atr * 3.0)
                    else:
                        stop_loss = entry + (atr * 1.5)
                        take_profit = entry - (atr * 3.0)
                    
                    hybrid_signal = {
                        "tipe": final_type,
                        "entry": round(entry, 2),
                        "stop_loss": round(stop_loss, 2),
                        "take_profit": round(take_profit, 2),
                        "confidence": round(lstm_confidence * 0.9, 4),  # Slight penalty for LSTM-only
                        "confluence_status": "LSTM_ONLY",
                        "technical_signal": "NONE",
                        "technical_confidence": 0,
                        "lstm_direction": lstm_direction,
                        "lstm_confidence": round(lstm_confidence, 4),
                        "alasan": f"[LSTM ONLY] Prediksi {lstm_direction} dengan confidence {lstm_confidence*100:.0f}%",
                        "timestamp": datetime.now().isoformat()
                    }
                    hybrid_signals.append(hybrid_signal)
        
        # 8. Generate recommendation
        if hybrid_signals:
            best_signal = hybrid_signals[0]
            recommendation = {
                "aksi": best_signal["tipe"],
                "kekuatan": "SANGAT KUAT" if best_signal["confluence_status"] == "STRONG" else "KUAT" if best_signal["confidence"] >= 0.70 else "SEDANG",
                "entry": best_signal["entry"],
                "stop_loss": best_signal["stop_loss"],
                "take_profit": best_signal["take_profit"],
                "alasan": best_signal["alasan"]
            }
        else:
            recommendation = {
                "aksi": "TUNGGU",
                "kekuatan": "LEMAH",
                "entry": None,
                "stop_loss": None,
                "take_profit": None,
                "alasan": "Tidak ada sinyal yang cukup kuat dari Technical maupun LSTM"
            }
        
        return {
            "status": "sukses",
            "symbol": symbol.upper(),
            "mode_trading": mode_trading,
            "interval": interval,
            "harga_terkini": current_price,
            "jumlah_candle": len(df_dengan_indikator),
            "hybrid_signals": hybrid_signals,
            "technical_analysis": {
                "jumlah_sinyal": len(sinyal_teknikal),
                "sinyal_terbaru": sinyal_teknikal[-1] if sinyal_teknikal else None
            },
            "lstm_prediction": lstm_prediction,
            "rekomendasi": recommendation,
            "indikator_terkini": {
                "rsi_6": round(df_dengan_indikator['rsi_6'].iloc[-1], 2) if 'rsi_6' in df_dengan_indikator.columns else None,
                "rsi_14": round(df_dengan_indikator['rsi_14'].iloc[-1], 2) if 'rsi_14' in df_dengan_indikator.columns else None,
                "ema_20": round(df_dengan_indikator['ema_20'].iloc[-1], 2) if 'ema_20' in df_dengan_indikator.columns else None,
                "ema_50": round(df_dengan_indikator['ema_50'].iloc[-1], 2) if 'ema_50' in df_dengan_indikator.columns else None,
                "ema_200": round(df_dengan_indikator['ema_200'].iloc[-1], 2) if 'ema_200' in df_dengan_indikator.columns else None,
                "atr_14": round(df_dengan_indikator['atr_14'].iloc[-1], 2) if 'atr_14' in df_dengan_indikator.columns else None,
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Gagal analisis hybrid: {err}")


# FastAPI standar tetap membutuhkan variabel bernama `app`.
# Kita map `app` ke `aplikasi` agar uvicorn bisa menjalankan backend ini.
app = aplikasi

