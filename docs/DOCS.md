# DOKUMENTASI LENGKAP
## Leon Liquidity Engine - Sistem Cerdas Analisis Trading Cryptocurrency

---

## DAFTAR ISI

1. [Pendahuluan](#1-pendahuluan)
2. [Arsitektur Sistem](#2-arsitektur-sistem)
3. [Instalasi & Setup](#3-instalasi--setup)
4. [Struktur Project](#4-struktur-project)
5. [Fitur Utama](#5-fitur-utama)
6. [Mode Trading](#6-mode-trading)
7. [Algoritma Sistem Cerdas](#7-algoritma-sistem-cerdas)
8. [Panduan Penggunaan](#8-panduan-penggunaan)
9. [API Reference](#9-api-reference)
10. [Interpretasi Hasil](#10-interpretasi-hasil)
11. [Troubleshooting & FAQ](#11-troubleshooting--faq)

---

## 1. PENDAHULUAN

### 1.1 Tentang Leon Liquidity Engine

Leon Liquidity Engine adalah **Sistem Cerdas** berbasis web yang dirancang untuk menganalisis data cryptocurrency dan menghasilkan sinyal trading (BELI/JUAL) berdasarkan indikator teknikal dan machine learning.

### 1.2 Latar Belakang

Trading cryptocurrency memerlukan analisis teknikal yang kompleks dan pengambilan keputusan yang cepat. Trader pemula sering kesulitan mengidentifikasi waktu yang tepat untuk membeli atau menjual aset. Sistem ini dirancang untuk membantu trader dengan:
- Menganalisis data historis dan real-time cryptocurrency
- Mengidentifikasi peluang trading berdasarkan indikator teknikal
- Memberikan rekomendasi sinyal BELI/JUAL dengan tingkat kepercayaan (confidence)
- Melakukan backtesting untuk validasi performa sistem
- Prediksi arah harga menggunakan LSTM Deep Learning

### 1.3 Fitur Utama

| Fitur | Deskripsi |
|-------|-----------|
| Live Trading | Analisis real-time dari Binance API |
| AI Prediction | Prediksi arah harga dengan LSTM Neural Network |
| Backtest Engine | Simulasi trading dengan data historis CSV |
| Data Manager | Upload dan kelola data CSV |
| Dashboard | Monitoring statistik dan performa |
| Cyberpunk UI | Interface futuristik dengan tema neon |

### 1.4 Komponen Sistem Cerdas

| Komponen | Deskripsi |
|----------|-----------|
| Knowledge Base | Aturan trading dari expert (RSI, EMA, S/R, Divergence) |
| Inference Engine | Mesin inferensi untuk generate sinyal |
| LSTM Predictor | Deep Learning untuk prediksi arah harga |
| Confidence Scoring | Perhitungan tingkat kepercayaan sinyal |
| Backtesting Engine | Simulasi dan validasi performa |

---

## 2. ARSITEKTUR SISTEM

### 2.1 Diagram Arsitektur

```
┌─────────────────────────────────────────────────────────────────────┐
│                         LEON LIQUIDITY ENGINE                        │
│                    Sistem Cerdas Trading Cryptocurrency              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────────────┐   │
│  │   FRONTEND   │    │   BACKEND    │    │   KNOWLEDGE BASE     │   │
│  │  (Cyberpunk) │◄──►│   (FastAPI)  │◄──►│   (Trading Rules)    │   │
│  └──────────────┘    └──────────────┘    └──────────────────────┘   │
│         │                   │                       │                │
│         ▼                   ▼                       ▼                │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────────────┐   │
│  │  Dashboard   │    │  Services:   │    │  Expert Rules:       │   │
│  │  Live Signal │    │  - Binance   │    │  - RSI Extreme       │   │
│  │  AI Predict  │    │  - LSTM      │    │  - EMA Alignment     │   │
│  │  Backtest    │    │  - Generator │    │  - Trend Filter      │   │
│  │  Data Mgr    │    │  - Backtest  │    │  - S/R Detection     │   │
│  └──────────────┘    └──────────────┘    │  - Divergence        │   │
│                             │            └──────────────────────┘   │
│                             ▼                                        │
│                      ┌──────────────┐                               │
│                      │  INFERENCE   │                               │
│                      │   ENGINE     │                               │
│                      │              │                               │
│                      │ ┌──────────┐ │                               │
│                      │ │Confluence│ │                               │
│                      │ │ Scoring  │ │                               │
│                      │ └──────────┘ │                               │
│                      │ ┌──────────┐ │                               │
│                      │ │Confidence│ │                               │
│                      │ │Calculator│ │                               │
│                      │ └──────────┘ │                               │
│                      │ ┌──────────┐ │                               │
│                      │ │ Signal   │ │                               │
│                      │ │Generator │ │                               │
│                      │ └──────────┘ │                               │
│                      └──────────────┘                               │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### 2.2 Teknologi yang Digunakan

| Komponen | Teknologi | Fungsi |
|----------|-----------|--------|
| Backend | Python 3.11+ | Bahasa pemrograman utama |
| Framework | FastAPI | REST API framework |
| Data Processing | Pandas, NumPy | Manipulasi data & komputasi |
| Machine Learning | TensorFlow/Keras | LSTM Neural Network |
| Real-time Data | Binance API | Data harga cryptocurrency |
| Frontend | HTML/CSS/JS | User interface |
| Charts | Chart.js | Visualisasi data |
| Notifications | SweetAlert2 | Alert & modal cyberpunk |
| Server | Uvicorn | ASGI server |

---

## 3. INSTALASI & SETUP

### 3.1 Persyaratan Sistem

**Hardware Minimum:**
- Processor: Intel Core i3 atau setara
- RAM: 4 GB
- Storage: 500 MB free space
- Koneksi internet

**Software Requirements:**
- Operating System: Windows 10/11, macOS, atau Linux
- Python: Versi 3.11 atau lebih baru
- Web Browser: Chrome, Firefox, Edge (versi terbaru)

### 3.2 Langkah Instalasi

```bash
# 1. Clone repository
git clone https://github.com/zeen-lien/Leon-Liquidity-Engine.git
cd Leon-Liquidity-Engine

# 2. Buat Virtual Environment (Opsional tapi Disarankan)
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# 3. Install Dependencies
pip install -r requirements.txt

# 4. Verifikasi Instalasi
python -c "import fastapi; import pandas; print('Instalasi berhasil!')"
```

### 3.3 Menjalankan Aplikasi

```bash
# Start Server
python -m uvicorn backend.app:app --reload --port 8000

# Akses Aplikasi
# Browser: http://127.0.0.1:8000
# API Docs: http://127.0.0.1:8000/docs

# Stop Server
# Tekan Ctrl + C di terminal
```

---

## 4. STRUKTUR PROJECT

```
Leon-Liquidity-Engine/
├── backend/                    # Backend API
│   ├── api/                   # API endpoints (future)
│   │   └── __init__.py
│   ├── core/                  # Konfigurasi inti
│   │   └── __init__.py
│   ├── models/                # Database models (future)
│   │   └── __init__.py
│   ├── services/              # Business logic
│   │   ├── binance_realtime.py   # Binance API integration
│   │   ├── lstm_predictor.py     # LSTM Deep Learning
│   │   ├── generator_sinyal_unified.py  # Signal generator
│   │   ├── praproses_data.py     # Data preprocessing
│   │   ├── backtesting_engine.py # Backtest engine
│   │   └── __init__.py
│   ├── utils/                 # Helper functions
│   │   └── __init__.py
│   └── app.py                 # Main FastAPI application
├── frontend/                   # Web interface
│   └── index.html             # Dashboard UI (Cyberpunk theme)
├── data/                      # Data storage
│   ├── uploads/              # Raw CSV files
│   ├── processed/            # Processed data with indicators
│   └── models/               # Trained ML models
├── docs/                      # Dokumentasi
│   ├── DOCS.md               # Dokumentasi lengkap (file ini)
│   ├── DESAIN_PERANCANGAN.md # Desain sistem
│   ├── MANUAL_BOOK.md        # Manual pengguna
│   └── PANDUAN_LENGKAP.md    # Panduan teknis
├── tests/                     # Test suite
│   └── __init__.py
├── .gitignore                 # Git ignore rules
├── requirements.txt           # Python dependencies
└── README.md                  # Project overview
```

---

## 5. FITUR UTAMA

### 5.1 Dashboard
Halaman utama yang menampilkan:
- Statistik total sinyal, win rate, avg P&L
- Real-time prices dari Binance API
- Chart distribusi hasil (Pie chart)
- Equity curve (Line chart)

### 5.2 Live Signals
Analisis real-time dari Binance API:
- Pilih cryptocurrency (BTC, ETH, BNB, SOL, XRP)
- Pilih mode trading (Aktif, Santai, Pasif)
- Generate sinyal BELI/JUAL dengan Entry, SL, TP
- Confidence score untuk setiap sinyal

### 5.3 AI Prediction
Prediksi arah harga dengan LSTM:
- Deep Learning Neural Network
- Prediksi arah: NAIK atau TURUN
- Confidence score
- Rekomendasi aksi (BELI/JUAL/TUNGGU)

### 5.4 Backtest Engine
Simulasi trading dengan data historis:
- Upload data CSV
- Test strategi dengan berbagai mode
- Statistik performa (Win Rate, P&L, Duration)
- Hasil per sinyal (HIT_TP, HIT_SL, TIMEOUT)

### 5.5 Data Manager
Kelola data CSV:
- Buat folder per cryptocurrency
- Upload file CSV
- Proses indikator teknikal
- Lihat daftar folder dan file

---

## 6. MODE TRADING

Sistem menggunakan data H1 (1 jam) dan menyediakan 3 mode trading:

### 6.1 Mode AKTIF (1-4 Jam)

| Parameter | Nilai |
|-----------|-------|
| RSI Period | 6 |
| RSI Oversold | 15 |
| RSI Overbought | 85 |
| EMA | 9, 20, 50 |
| ATR Period | 6 |
| Risk-Reward | 2.0 |
| Target Durasi | 1-4 jam |

**Cocok untuk:** Trading aktif, quick trend catching

### 6.2 Mode SANTAI (4-12 Jam)

| Parameter | Nilai |
|-----------|-------|
| RSI Period | 8 |
| RSI Oversold | 18 |
| RSI Overbought | 82 |
| EMA | 20, 50, 200 |
| ATR Period | 10 |
| Risk-Reward | 2.5 |
| Target Durasi | 4-12 jam |

**Cocok untuk:** Day trading, work-life balance

### 6.3 Mode PASIF (12-24 Jam)

| Parameter | Nilai |
|-----------|-------|
| RSI Period | 14 |
| RSI Oversold | 15 |
| RSI Overbought | 85 |
| EMA | 50, 100, 200 |
| ATR Period | 14 |
| Risk-Reward | 3.0 |
| Target Durasi | 12-24 jam |

**Cocok untuk:** Swing trading, conservative approach

---

## 7. ALGORITMA SISTEM CERDAS

### 7.1 Knowledge Base (Basis Pengetahuan)

Aturan trading dari expert yang dikodekan dalam sistem:

| No | Aturan | Deskripsi |
|----|--------|-----------|
| 1 | RSI Oversold | RSI <= threshold menandakan jenuh jual |
| 2 | RSI Overbought | RSI >= threshold menandakan jenuh beli |
| 3 | EMA Alignment | EMA Fast > EMA Mid = trend naik |
| 4 | Trend Filter | Harga > EMA200 = uptrend |
| 5 | Support/Resistance | Deteksi level S/R dari pivot points |
| 6 | Divergence | Harga vs RSI divergence = reversal signal |

### 7.2 Inference Engine (Mesin Inferensi)

```
INPUT: Data OHLCV + Indikator Teknikal
         │
         ▼
┌─────────────────────────────────────┐
│     CEK KONDISI (6 ATURAN)          │
│                                     │
│  1. RSI Oversold/Overbought?        │
│  2. EMA Alignment?                  │
│  3. Price vs EMA Fast?              │
│  4. Trend Filter EMA200?            │
│  5. Dekat Support/Resistance?       │
│  6. Candle Bullish/Bearish?         │
│                                     │
└─────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│     HITUNG CONFLUENCE               │
│                                     │
│  Jumlah kondisi terpenuhi: X/6      │
│  Minimum untuk sinyal: 4/6          │
│                                     │
└─────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│     HITUNG CONFIDENCE               │
│                                     │
│  Base: 35%                          │
│  + Confluence bonus: 8-20%          │
│  + Divergence bonus: 12%            │
│  + S/R proximity bonus: 5-15%       │
│  ─────────────────────────          │
│  Total: 35% - 80%                   │
│                                     │
└─────────────────────────────────────┘
         │
         ▼
OUTPUT: Sinyal BELI/JUAL + Confidence
```

### 7.3 Algoritma Confidence Scoring

```python
ALGORITMA: Hitung_Confidence_Jujur

INPUT:
  - jumlah_confluence: int (0-6)
  - ada_divergence: bool
  - jarak_support_persen: float

OUTPUT:
  - confidence: float (0.35 - 0.80)

PROSES:
1. SET confidence = 0.35 (base conservative)

2. HITUNG rasio_confluence = jumlah_confluence / 6

3. TAMBAH bonus confluence:
   - JIKA rasio >= 1.0 (6/6): confidence += 0.20
   - JIKA rasio >= 0.83 (5/6): confidence += 0.15
   - JIKA rasio >= 0.67 (4/6): confidence += 0.12
   - JIKA rasio >= 0.50 (3/6): confidence += 0.08

4. JIKA ada_divergence:
   confidence += 0.12

5. JIKA jarak_support < 0.5%: confidence += 0.15
   JIKA jarak_support < 1.0%: confidence += 0.10
   JIKA jarak_support < 2.0%: confidence += 0.08

6. RETURN MIN(0.80, confidence)
```

### 7.4 Perbedaan Live Signals vs AI Prediction

| Feature | Live Signals | AI Prediction |
|---------|--------------|---------------|
| Teknologi | Indikator Teknikal | LSTM Deep Learning |
| Basis | Rules-based confluence | Pattern recognition |
| Output | BELI/JUAL + Entry/SL/TP | NAIK/TURUN + Confidence |
| Use Case | Trading aktif | Analisis jangka menengah |
| Data Source | Binance Real-time | Historical patterns |

---

## 8. PANDUAN PENGGUNAAN


### 8.1 Dashboard

Dashboard adalah halaman utama yang menampilkan ringkasan statistik sistem.

**Informasi yang Ditampilkan:**
- Total Signals: Jumlah sinyal yang dihasilkan
- Win Rate: Persentase sinyal yang profit
- Avg P&L: Rata-rata profit/loss
- Active Pairs: Jumlah cryptocurrency aktif
- Real-time Prices: Harga terkini dari Binance
- Charts: Distribusi hasil dan equity curve

### 8.2 Live Signals

**Langkah-langkah:**
1. Klik menu "Live Signals" di sidebar
2. Pilih cryptocurrency dari dropdown (BTC, ETH, BNB, SOL, XRP)
3. Pilih mode trading (Aktif, Santai, Pasif)
4. Klik "GENERATE SIGNAL"
5. Lihat hasil sinyal dengan Entry, SL, TP, dan Confidence

**Output:**
- Pair: Pasangan mata uang
- Signal: BELI atau JUAL
- Entry: Harga masuk posisi
- Stop Loss: Batas kerugian
- Take Profit: Target keuntungan
- Confidence: Tingkat kepercayaan (35-80%)
- Reason: Alasan sinyal dihasilkan

### 8.3 AI Prediction

**Langkah-langkah:**
1. Klik menu "AI Prediction" di sidebar
2. Pilih cryptocurrency dari dropdown
3. Klik "ANALYZE WITH AI"
4. Lihat hasil prediksi arah harga

**Output:**
- Direction: NAIK (Bullish) atau TURUN (Bearish)
- Confidence: Tingkat kepercayaan prediksi
- Current Price: Harga terkini
- Recommendation: BELI, JUAL, atau TUNGGU
- Indicators: RSI, EMA20, EMA50

### 8.4 Backtest Engine

**Langkah-langkah:**
1. Klik menu "Backtest Engine" di sidebar
2. Pilih folder data dari dropdown
3. Pilih mode trading
4. Klik "EXECUTE BACKTEST"
5. Lihat hasil backtest dan statistik

**Output:**
- Total Signals: Jumlah sinyal yang dihasilkan
- Win Rate: Persentase sinyal profit
- HIT TP: Sinyal yang mencapai Take Profit
- HIT SL: Sinyal yang mencapai Stop Loss
- Tabel detail per sinyal dengan P&L

### 8.5 Data Manager

**Upload CSV:**
1. Klik menu "Data Manager" di sidebar
2. Pilih folder tujuan atau buat folder baru
3. Klik "BROWSE" untuk pilih file CSV
4. Klik "UPLOAD FILE"

**Proses Indikator:**
1. Pilih folder yang sudah ada data
2. Klik "PROCESS INDICATORS"
3. Tunggu hingga selesai

**Format CSV yang Diterima:**
```csv
open_time,open,high,low,close,volume
1704326400000,42000.5,42500.0,41800.0,42300.0,1500.5
1704330000000,42300.0,42800.0,42100.0,42600.0,1800.2
```

**Sumber Data:**
- Binance Vision: https://data.binance.vision/
- Download data kline/spot dengan interval 1h (1 jam)

---

## 9. API REFERENCE

### 9.1 Health Check
```http
GET /cek-kesehatan
```
Response: `{"status": "sehat", "versi": "2.1"}`

### 9.2 Folder Management

**Daftar Folder:**
```http
GET /folder/daftar
```

**Buat Folder:**
```http
POST /folder/buat
Content-Type: application/json

{"nama_folder": "BTC"}
```

**Rename Folder:**
```http
PUT /folder/rename
Content-Type: application/json

{"nama_lama": "BTC", "nama_baru": "BTCUSDT"}
```

**Hapus Folder:**
```http
DELETE /folder/hapus/{nama_folder}
```

### 9.3 Upload & File Management

**Upload CSV:**
```http
POST /unggah-csv/?folder=BTC
Content-Type: multipart/form-data

berkas: <file.csv>
```

**Daftar File:**
```http
GET /unggah-csv/daftar/{folder}
```

**Hapus File:**
```http
DELETE /unggah-csv/hapus/{folder}/{nama_file}
```

### 9.4 Preprocessing

**Proses Indikator:**
```http
POST /pra-proses/indikator/
Content-Type: application/json

{"folder": "BTC"}
```

### 9.5 Signal Generation

**Generate Sinyal (Backtest):**
```http
POST /sinyal/generate
Content-Type: application/json

{
  "folder": "BTC",
  "mode_trading": "santai",
  "confidence_minimum": 0.60
}
```

### 9.6 Binance Real-time

**Get Prices:**
```http
GET /binance/prices
```

**Analyze Symbol:**
```http
POST /binance/analyze/{symbol}?mode_trading=santai
```

### 9.7 LSTM Prediction

**Get Prediction:**
```http
GET /lstm/predict/{symbol}
```

### 9.8 Response Format

**Sinyal Trading:**
```json
{
  "status": "sukses",
  "jumlah_sinyal": 15,
  "sinyal": [
    {
      "tipe": "BELI",
      "entry": 97992.0,
      "stop_loss": 97340.76,
      "take_profit": 99620.09,
      "confidence": 0.65,
      "alasan": "[Mode Santai] Sinyal BELI, Konfluensi: 5/6",
      "timestamp": "2025-01-04T14:00:00",
      "pair": "BTCUSDT",
      "backtest_result": "HIT_TP",
      "pnl_percent": 2.15
    }
  ],
  "backtest_statistics": {
    "total_signals": 15,
    "win_rate": 73.3,
    "hit_tp": 11,
    "hit_sl": 4,
    "avg_pnl": 1.85
  }
}
```

**AI Prediction:**
```json
{
  "status": "sukses",
  "symbol": "BTCUSDT",
  "harga_terkini": 97500.0,
  "prediksi": {
    "direction": "UP",
    "confidence": 0.72,
    "rsi": 45.5,
    "ema_20": 96800.0,
    "ema_50": 95500.0
  },
  "rekomendasi": {
    "aksi": "BELI",
    "alasan": "Trend bullish dengan momentum kuat"
  }
}
```

---

## 10. INTERPRETASI HASIL

### 10.1 Confidence Score

| Range | Kategori | Rekomendasi |
|-------|----------|-------------|
| 70% - 80% | Tinggi | Sinyal sangat kuat, layak dipertimbangkan |
| 60% - 70% | Sedang | Sinyal cukup kuat, perlu konfirmasi |
| < 60% | Rendah | Sinyal lemah, sebaiknya diabaikan |

**Catatan:** Confidence tidak pernah 100% karena sistem dirancang dengan prinsip kejujuran. Tidak ada sinyal yang pasti profit.

### 10.2 Hasil Backtest

| Status | Deskripsi |
|--------|-----------|
| HIT_TP | Sinyal mencapai Take Profit (profit) |
| HIT_SL | Sinyal mencapai Stop Loss (loss) |
| TIMEOUT | Sinyal tidak selesai dalam 168 jam |

### 10.3 Statistik Performa

- **Win Rate**: Persentase sinyal profit = HIT_TP / (HIT_TP + HIT_SL) × 100%
- **Avg P&L**: Rata-rata profit/loss per sinyal
- **Avg Duration**: Rata-rata waktu sinyal selesai (jam)

### 10.4 Rekomendasi Penggunaan

**Untuk Pemula:**
- Gunakan mode SANTAI (lebih seimbang)
- Fokus pada sinyal dengan confidence >= 65%
- Perhatikan win rate minimal 70%

**Untuk Intermediate:**
- Gunakan mode AKTIF untuk trading lebih sering
- Kombinasikan Live Signals dengan AI Prediction
- Perhatikan alasan sinyal untuk pembelajaran

**Untuk Advanced:**
- Gunakan mode PASIF untuk swing trading
- Analisis divergence untuk konfirmasi tambahan
- Sesuaikan parameter sesuai kondisi pasar

---

## 11. TROUBLESHOOTING & FAQ

### 11.1 Server Tidak Bisa Start

**Masalah:** Error saat menjalankan uvicorn

**Solusi:**
```bash
# Pastikan dependencies terinstall
pip install -r requirements.txt

# Pastikan berada di folder yang benar
cd Leon-Liquidity-Engine

# Coba jalankan ulang
python -m uvicorn backend.app:app --reload --port 8000
```

### 11.2 Upload CSV Gagal

**Solusi:**
1. Pastikan format file adalah .csv
2. Pastikan kolom sesuai: open_time, open, high, low, close, volume
3. Pastikan tidak ada karakter khusus di nama file
4. Pastikan folder tujuan sudah dibuat

### 11.3 Tidak Ada Sinyal yang Dihasilkan

**Solusi:**
1. Pastikan data sudah diproses dengan indikator
2. Coba mode trading yang berbeda
3. Pastikan data memiliki minimal 200 baris
4. Market mungkin sedang sideways (normal)

### 11.4 AI Prediction Error

**Solusi:**
1. Pastikan koneksi internet aktif
2. Binance API mungkin sedang maintenance
3. Coba refresh halaman

### 11.5 FAQ

**Q: Apakah sistem ini bisa digunakan untuk trading real?**
A: Sistem ini dirancang sebagai alat bantu analisis dan pembelajaran. Untuk trading real, selalu lakukan analisis tambahan dan manajemen risiko yang tepat.

**Q: Berapa akurasi sistem ini?**
A: Berdasarkan backtesting, sistem mencapai win rate 70-90% tergantung mode trading dan kondisi pasar. Namun, performa masa lalu tidak menjamin hasil di masa depan.

**Q: Apa perbedaan Live Signals dan AI Prediction?**
A: Live Signals menggunakan indikator teknikal (RSI, EMA) untuk generate sinyal BELI/JUAL dengan Entry/SL/TP. AI Prediction menggunakan LSTM Neural Network untuk prediksi arah harga (NAIK/TURUN).

**Q: Mengapa confidence tidak pernah 100%?**
A: Sistem dirancang dengan prinsip kejujuran. Tidak ada sinyal yang 100% pasti profit. Range 35-80% mencerminkan realitas trading.

**Q: Data dari mana yang bisa digunakan?**
A: Sistem menerima data OHLCV dalam format CSV. Sumber yang direkomendasikan adalah Binance Vision (data.binance.vision) dengan interval 1 jam (1h).

---

## LAMPIRAN

### A. Indikator Teknikal

**RSI (Relative Strength Index)**
- Mengukur momentum harga
- Range: 0 - 100
- Oversold: < 30 (extreme: < 15)
- Overbought: > 70 (extreme: > 85)

**EMA (Exponential Moving Average)**
- Mengukur trend harga
- EMA Fast > EMA Slow = Uptrend
- EMA Fast < EMA Slow = Downtrend

**ATR (Average True Range)**
- Mengukur volatilitas pasar
- Digunakan untuk menentukan Stop Loss dan Take Profit

**Support/Resistance**
- Support: Level harga dimana harga cenderung memantul naik
- Resistance: Level harga dimana harga cenderung memantul turun

**Divergence**
- Bullish Divergence: Harga turun tapi RSI naik (sinyal reversal naik)
- Bearish Divergence: Harga naik tapi RSI turun (sinyal reversal turun)

### B. Python Dependencies

```
fastapi>=0.100.0
uvicorn>=0.23.0
pandas>=2.0.0
numpy>=1.24.0
python-multipart>=0.0.6
httpx>=0.24.0
tensorflow>=2.13.0 (optional, untuk LSTM)
```

### C. Referensi

1. RSI (Relative Strength Index) - J. Welles Wilder Jr.
2. EMA (Exponential Moving Average) - Technical Analysis
3. ATR (Average True Range) - J. Welles Wilder Jr.
4. LSTM Networks - Hochreiter & Schmidhuber (1997)
5. Support/Resistance - Price Action Analysis

---

*Dokumentasi Leon Liquidity Engine v2.1*
*Sistem Cerdas untuk Analisis Trading Cryptocurrency*
*© 2025 - Dibuat untuk tugas Sistem Cerdas*
