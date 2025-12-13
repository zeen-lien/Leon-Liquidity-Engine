# DOKUMENTASI LENGKAP
## Leon Liquidity Engine v3.0 - Sistem Trading Cryptocurrency Cyberpunk

---

## DAFTAR ISI

1. [Pendahuluan](#1-pendahuluan)
2. [Arsitektur Sistem](#2-arsitektur-sistem)
3. [Instalasi & Setup](#3-instalasi--setup)
4. [Struktur Project](#4-struktur-project)
5. [Fitur Utama](#5-fitur-utama)
6. [Mode Trading & Market Types](#6-mode-trading--market-types)
7. [Signal Tracking System](#7-signal-tracking-system)
8. [Entry Size Management](#8-entry-size-management)
9. [Algoritma Sistem Cerdas](#9-algoritma-sistem-cerdas)
10. [Panduan Penggunaan](#10-panduan-penggunaan)
11. [API Reference](#11-api-reference)
12. [Interpretasi Hasil](#12-interpretasi-hasil)
13. [Troubleshooting & FAQ](#13-troubleshooting--faq)

---

## 1. PENDAHULUAN

### 1.1 Tentang Leon Liquidity Engine v3.0

Leon Liquidity Engine v3.0 adalah **Sistem Trading Cryptocurrency** berbasis web dengan tema cyberpunk yang dirancang untuk menganalisis data real-time dan menghasilkan sinyal trading (BELI/JUAL) dengan sistem tracking otomatis dan manajemen entry size yang canggih.

### 1.2 Fitur Revolusioner v3.0

**🚀 NEW FEATURES:**
- **Multi-Signal Support**: Satu symbol bisa punya 3 signals berbeda (AKTIF, SANTAI, PASIF) secara bersamaan
- **SPOT vs FUTURES**: Diferensiasi market dengan strategi khusus untuk investor jangka panjang (SPOT) dan trader aktif (FUTURES)
- **Entry Size Management**: Sistem manajemen modal dengan persentase entry dan tracking P&L dalam dollar
- **Active Signal Tracking**: Real-time monitoring signals dengan auto-refresh dan filter canggih
- **Signal History**: Riwayat lengkap semua signals dengan statistik performa
- **Smart Price Formatting**: Format harga dinamis untuk small cap coins (PEPE, SHIB, dll)
- **Auto Signal Service**: Background service untuk monitoring SL/TP secara otomatis

### 1.3 Fitur Utama v3.0

| Fitur | Deskripsi | Status |
|-------|-----------|--------|
| **Dashboard Command Center** | Real-time stats, watchlist, quick signal generator | ✅ ACTIVE |
| **Live Signals (Hybrid)** | Analisis real-time dengan Technical + LSTM AI | ✅ ACTIVE |
| **Active Tracking** | Monitor signals aktif dengan filter dan real-time updates | ✅ ACTIVE |
| **Signal History** | Riwayat lengkap dengan statistik dan filter | ✅ ACTIVE |
| **Market Chart** | Live candlestick chart dari Binance WebSocket | ✅ ACTIVE |
| **Backtest Engine** | Simulasi trading dengan data historis | ✅ ACTIVE |
| **Data Manager** | Upload dan kelola data CSV | ✅ ACTIVE |
| **ML Training** | AI prediction dengan LSTM Neural Network | ✅ ACTIVE |
| **Cyberpunk UI** | Interface futuristik dengan neon theme | ✅ ACTIVE |

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

## 6. MODE TRADING & MARKET TYPES

### 6.1 Market Types

**FUTURES Market:**
- Support BELI dan JUAL signals (long & short)
- Take Profit: 3x ATR
- Interval berdasarkan mode trading
- Cocok untuk: Active trading, scalping, swing trading

**SPOT Market:**
- Hanya BELI signals (no shorting)
- Take Profit: 5x ATR (lebih lebar untuk long-term)
- Interval: 1D (daily) untuk semua mode
- Mode khusus: "INVESTOR" untuk buy & hold strategy
- Cocok untuk: Long-term investment, DCA strategy

### 6.2 Mode Trading dengan Interval Mapping

| Mode | Interval (FUTURES) | Interval (SPOT) | Target Durasi | Risk-Reward |
|------|-------------------|-----------------|---------------|-------------|
| **AKTIF** | 15m | 1D | 1-4 jam | 2.0x |
| **SANTAI** | 1h | 1D | 4-12 jam | 2.5x |
| **PASIF** | 4h | 1D | 12-24 jam | 3.0x |
| **INVESTOR** | - | 1D | 1-30 hari | 5.0x |

### 6.3 Multi-Signal Support

**REVOLUTIONARY FEATURE**: Satu symbol bisa memiliki multiple signals dengan mode berbeda secara bersamaan!

**Contoh:**
```
BTCUSDT:
├── Signal AKTIF (15m) - Entry: $97,500 - Status: OPEN
├── Signal SANTAI (1h) - Entry: $97,200 - Status: OPEN  
└── Signal PASIF (4h) - Entry: $96,800 - Status: OPEN
```

**Rules:**
- Maksimal 1 signal per mode per symbol
- Jika ada signal OPEN untuk mode yang sama, harus tunggu close dulu
- Bisa generate signal mode lain tanpa menunggu

### 6.4 Parameter Detail per Mode

**Mode AKTIF (Quick Scalping):**
| Parameter | FUTURES | SPOT |
|-----------|---------|------|
| Interval | 15m | 1D |
| RSI Period | 6 | 14 |
| RSI Oversold | 15 | 30 |
| RSI Overbought | 85 | 70 |
| EMA | 9, 20, 50 | 20, 50, 200 |
| ATR Multiplier | 2.0x | 5.0x |
| Target | 1-4 jam | 1-7 hari |

**Mode SANTAI (Balanced Trading):**
| Parameter | FUTURES | SPOT |
|-----------|---------|------|
| Interval | 1h | 1D |
| RSI Period | 8 | 14 |
| RSI Oversold | 18 | 30 |
| RSI Overbought | 82 | 70 |
| EMA | 20, 50, 200 | 50, 100, 200 |
| ATR Multiplier | 2.5x | 5.0x |
| Target | 4-12 jam | 3-14 hari |

**Mode PASIF (Swing Trading):**
| Parameter | FUTURES | SPOT |
|-----------|---------|------|
| Interval | 4h | 1D |
| RSI Period | 14 | 21 |
| RSI Oversold | 15 | 25 |
| RSI Overbought | 85 | 75 |
| EMA | 50, 100, 200 | 100, 200, 300 |
| ATR Multiplier | 3.0x | 5.0x |
| Target | 12-24 jam | 7-30 hari |

---

## 7. SIGNAL TRACKING SYSTEM

### 7.1 Auto Signal Service

**Background Service** yang berjalan otomatis untuk monitoring semua signals aktif:

```
┌─────────────────────────────────────────────────────────────┐
│                    AUTO SIGNAL SERVICE                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────┐  │
│  │   BINANCE   │    │  DATABASE   │    │   WEBSOCKET     │  │
│  │  WEBSOCKET  │◄──►│   SIGNALS   │◄──►│   FRONTEND      │  │
│  │ (Real-time) │    │   (SQLite)  │    │ (Live Updates)  │  │
│  └─────────────┘    └─────────────┘    └─────────────────┘  │
│         │                   │                     │         │
│         ▼                   ▼                     ▼         │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │              MONITORING ENGINE                          │ │
│  │                                                         │ │
│  │  • Check SL/TP setiap detik                            │ │
│  │  • Update highest/lowest price                         │ │
│  │  • Calculate real-time P&L                             │ │
│  │  • Auto close signals (HIT_TP/HIT_SL)                  │ │
│  │  • Expire old signals (>168 hours)                     │ │
│  │  • Send notifications                                   │ │
│  │                                                         │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 7.2 Signal Status Lifecycle

```
OPEN ──────┐
           │
           ├─► HIT_TP (Take Profit reached) ✅
           │
           ├─► HIT_SL (Stop Loss reached) ❌
           │
           ├─► EXPIRED (>168 hours timeout) ⏰
           │
           └─► CANCELLED (Manual close) 🚫
```

### 7.3 Real-time Features

**Live Price Updates:**
- WebSocket connection ke Binance
- Update harga setiap detik
- Automatic reconnection jika disconnect

**Active Tracking Page:**
- Real-time P&L calculation
- Progress bar ke TP/SL
- Duration counter
- Filter by Market/Mode/Type
- Auto-refresh setiap 5 detik

**Dashboard Integration:**
- Live active signals count
- Real-time statistics
- Performance metrics
- Equity simulation

### 7.4 Database Schema

**Signals Table:**
```sql
CREATE TABLE signals (
    id INTEGER PRIMARY KEY,
    symbol VARCHAR(20) NOT NULL,
    market_type VARCHAR(7) DEFAULT 'FUTURES',
    signal_type VARCHAR(4) NOT NULL,
    entry_price FLOAT NOT NULL,
    stop_loss FLOAT NOT NULL,
    take_profit FLOAT NOT NULL,
    confidence FLOAT NOT NULL,
    mode_trading VARCHAR(20) DEFAULT 'santai',
    
    -- Entry Size Management
    modal_total FLOAT,      -- Total modal user
    entry_pct FLOAT,        -- Persentase entry dari modal  
    entry_amount FLOAT,     -- Jumlah dollar yang dientry
    
    -- Timestamps
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    closed_at DATETIME,
    
    -- Status & Results
    status VARCHAR(9) DEFAULT 'OPEN',
    exit_price FLOAT,
    pnl_percent FLOAT,
    pnl_usdt FLOAT,
    duration_minutes INTEGER,
    
    -- Price Tracking
    highest_price FLOAT,    -- Highest since entry
    lowest_price FLOAT,     -- Lowest since entry
    
    -- Analysis Data
    confluence_status VARCHAR(20),
    technical_confidence FLOAT,
    lstm_confidence FLOAT,
    lstm_direction VARCHAR(10),
    alasan TEXT
);
```

---

## 8. ENTRY SIZE MANAGEMENT

### 8.1 Konsep Entry Size

**Entry Size** adalah sistem manajemen modal yang memungkinkan user menentukan berapa persen dari total modal yang akan digunakan untuk setiap signal.

**Formula:**
```
Entry Amount ($) = Modal Total ($) × Entry Percentage (%) ÷ 100

Contoh:
Modal Total: $1,000
Entry Percentage: 10%
Entry Amount: $1,000 × 10% = $100
```

### 8.2 P&L Calculation

**Profit/Loss dalam Dollar:**
```
P&L ($) = Entry Amount ($) × P&L Percentage (%) ÷ 100

Contoh Signal BELI:
Entry: $97,000
Current: $98,940
P&L%: +2.0%
Entry Amount: $100
P&L ($): $100 × 2.0% = +$2.00
```

### 8.3 Implementation

**Dashboard Quick Signal:**
```html
<div class="form-group">
    <label>ENTRY SIZE</label>
    <div style="display:flex;gap:6px;">
        <input id="quick-modal" value="1000" placeholder="Modal ($)">
        <input id="quick-entry-pct" value="10" placeholder="Pct (%)">
        <span id="quick-entry-amount">$100</span>
    </div>
</div>
```

**Live Signals Page:**
```html
<div class="form-group">
    <label>ENTRY SIZE (% dari Modal)</label>
    <div class="input-group">
        <input id="signal-modal" placeholder="Modal ($)" value="1000">
        <input id="signal-entry-pct" placeholder="%" value="10">
        <span id="signal-entry-amount">$100</span>
    </div>
</div>
```

**Active Tracking Display:**
```html
<div class="active-signal-card">
    <div class="entry-info">
        <span>ENTRY SIZE</span>
        <span>${entryAmount.toFixed(0)}</span>
    </div>
    <div class="pnl-info">
        <span>P&L ($)</span>
        <span style="color:${pnlColor}">${pnlSign}$${Math.abs(pnlDollar).toFixed(2)}</span>
    </div>
</div>
```

### 8.4 Fallback System

**Old Signals (NULL entry_amount):**
- Menggunakan nilai dari `tracking-modal` input di Active Tracking page
- Semua old signals akan menampilkan entry size yang sama
- Ini adalah expected behavior

**New Signals:**
- Menyimpan `modal_total`, `entry_pct`, dan `entry_amount` ke database
- Menampilkan entry size sesuai yang disimpan
- P&L calculation menggunakan entry_amount yang tersimpan

### 8.5 Benefits

1. **Risk Management**: User bisa kontrol exposure per signal
2. **Portfolio Tracking**: Total P&L dalam dollar, bukan hanya percentage
3. **Realistic Simulation**: Equity curve berdasarkan actual dollar amounts
4. **Flexible Sizing**: Bisa adjust entry size per signal sesuai confidence level

---

## 9. ALGORITMA SISTEM CERDAS

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

## 10. PANDUAN PENGGUNAAN

### 10.1 Dashboard Command Center

**Fitur Utama:**
- **Stats Grid**: Total signals, win rate, avg P&L, active signals
- **Performance Summary**: Real-time statistics dengan refresh button
- **Watchlist**: Favorite pairs dengan live prices dari Binance
- **Quick Signal**: Generate signal langsung dari dashboard
- **Active Signals**: Preview signals yang sedang berjalan
- **Charts**: Pie chart distribusi hasil & equity simulation

**Quick Signal Generator:**
1. Pilih Symbol (BTC, ETH, BNB, SOL, XRP)
2. Pilih Market Type (FUTURES/SPOT)
3. Pilih Mode Trading (AKTIF/SANTAI/PASIF atau INVESTOR untuk SPOT)
4. Set Entry Size (Modal + Percentage)
5. Klik "GENERATE NOW"
6. Konfirmasi untuk "SAVE & TRACK"

### 10.2 Live Signals (Hybrid Analysis)

**Revolutionary Hybrid System**: Kombinasi Technical Analysis + LSTM AI

**Langkah-langkah:**
1. Klik menu "Live Signals"
2. **Pilih Market Type**: FUTURES atau SPOT
3. **Cari Symbol**: Ketik nama coin (BTC, ETH, PEPE, dll)
4. **Set Entry Size**: Modal total dan persentase entry
5. **Pilih Mode Trading**: 
   - FUTURES: AKTIF (15m), SANTAI (1h), PASIF (4h)
   - SPOT: Semua mode menggunakan interval 1D (INVESTOR)
6. Klik "GENERATE HYBRID SIGNAL"

**Output Hybrid:**
- **Technical Confluence**: Berapa indikator yang align (X/6)
- **LSTM AI Prediction**: Direction + Confidence dari Neural Network
- **Combined Signal**: BELI/JUAL dengan Entry/SL/TP
- **Confidence Score**: Gabungan technical + AI (35-80%)
- **Detailed Reason**: Penjelasan lengkap kenapa signal dihasilkan

**Multi-Signal Support:**
- Bisa generate signal berbeda untuk mode berbeda
- Contoh: BTCUSDT AKTIF + BTCUSDT SANTAI + BTCUSDT PASIF bersamaan
- Sistem akan reject jika sudah ada signal OPEN untuk mode yang sama

### 10.3 Active Tracking (Real-time Monitoring)

**Fitur Canggih:**
- **Real-time Updates**: Auto-refresh setiap 5 detik
- **Live P&L**: Profit/Loss dalam percentage dan dollar
- **Progress Bars**: Visual progress menuju TP atau SL
- **Duration Counter**: Berapa lama signal sudah berjalan
- **Advanced Filters**: Filter by Market, Mode, Type
- **Modal Input**: Fallback entry size untuk old signals

**Filter System:**
```
Market Filter: All | FUTURES | SPOT
Mode Filter: All | AKTIF | SANTAI | PASIF  
Type Filter: All | BELI | JUAL
```

**Signal Card Information:**
- Symbol + Market Type + Mode badge
- Entry Time (Jakarta timezone)
- Entry Size dalam dollar
- Current Price vs Entry Price
- Real-time P&L (% dan $)
- Progress to TP/SL dengan visual bar
- Duration counter
- Action buttons (Close manual jika perlu)

### 10.4 Signal History (Complete Records)

**Comprehensive History System:**

**Stats Summary:**
- Total Closed Signals
- HIT TP vs HIT SL count
- Overall Win Rate
- Total Profit vs Total Loss dalam dollar

**Advanced Filters:**
```
Status: All | HIT_TP | HIT_SL | EXPIRED | CANCELLED
Market: All | FUTURES | SPOT
Type: All | BELI | JUAL
```

**History Table Columns:**
- Symbol (dengan market type dan mode)
- Signal Type (BELI/JUAL dengan color coding)
- Status (HIT_TP=green, HIT_SL=red, etc)
- Entry Price vs Exit Price
- P&L Percentage dan P&L Dollar
- Entry Size yang digunakan
- Duration (berapa lama signal berjalan)
- Closed Date (kapan signal selesai)

### 10.5 Market Chart (Live Binance Data)

**Real-time Candlestick Chart:**
- **Live WebSocket**: Data langsung dari Binance
- **Multiple Symbols**: BTC, ETH, BNB, SOL, XRP, DOGE, ADA, AVAX, PEPE
- **Multiple Timeframes**: 1m, 5m, 15m, 1h, 4h, 1d
- **Real-time Ticker**: Price, 24h change, high/low
- **Auto Reconnection**: Jika WebSocket disconnect

**Chart Features:**
- Candlestick visualization dengan Chart.js
- Real-time price updates
- Volume data
- Responsive design
- Status indicator (CONNECTING/LIVE/DISCONNECTED)

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

## 11. API REFERENCE

### 11.1 Health Check
```http
GET /cek-kesehatan
```
Response: `{"status": "sehat", "versi": "3.0"}`

### 11.2 Signal Management

**Create Signal:**
```http
POST /signals/create
Content-Type: application/json

{
  "symbol": "BTCUSDT",
  "market_type": "FUTURES",
  "signal_type": "BELI", 
  "entry_price": 97500.0,
  "stop_loss": 95000.0,
  "take_profit": 102500.0,
  "confidence": 0.75,
  "mode_trading": "santai",
  "modal_total": 1000.0,
  "entry_pct": 10.0,
  "entry_amount": 100.0,
  "alasan": "RSI oversold + EMA alignment"
}
```

**Get Active Signals:**
```http
GET /signals/active
```

**Get Signal History:**
```http
GET /signals/history?status=HIT_TP&market_type=FUTURES&limit=50
```

**Live Tracking:**
```http
GET /signals/tracking/live
```

**Performance Summary:**
```http
GET /signals/performance/summary
```

**Close Signal:**
```http
POST /signals/close/{signal_id}?exit_price=98500&status=HIT_TP
```

### 11.3 Auto Signal Service

**Start Auto Tracking:**
```http
POST /signals/auto/start
```

**Stop Auto Tracking:**
```http
POST /signals/auto/stop
```

**Get Service Status:**
```http
GET /signals/auto/status
```

**Check Expired Signals:**
```http
POST /signals/auto/check-expired?max_hours=168
```

### 11.4 Favorites Management

**Add to Favorites:**
```http
POST /signals/favorites/add
Content-Type: application/json

{"symbol": "BTCUSDT", "market_type": "FUTURES"}
```

**Get Favorites:**
```http
GET /signals/favorites
```

**Remove from Favorites:**
```http
DELETE /signals/favorites/{symbol}
```

### 11.5 Binance Integration

**Real-time Prices:**
```http
GET /binance/prices
```

**24h Ticker:**
```http
GET /binance/ticker24h/{symbol}
```

**Search Symbols:**
```http
GET /binance/search?query=BTC&market=FUTURES
```

**Kline Data:**
```http
GET /binance/klines/{symbol}?interval=1h&limit=100
```

### 11.6 Hybrid Analysis (NEW)

**Generate Hybrid Signal:**
```http
POST /hybrid/analyze/{symbol}?mode_trading=santai&interval=1h&market_type=FUTURES
```

Response:
```json
{
  "status": "sukses",
  "symbol": "BTCUSDT",
  "harga_terkini": 97500.0,
  "indikator_terkini": {
    "rsi_14": 45.2,
    "ema_20": 96800.0,
    "ema_50": 95500.0,
    "atr_14": 1250.0
  },
  "lstm_prediction": {
    "direction": "UP",
    "confidence": 0.72,
    "next_candles": [98000, 98500, 99000]
  },
  "hybrid_signals": [
    {
      "tipe": "BELI",
      "entry": 97500.0,
      "stop_loss": 95000.0,
      "take_profit": 102500.0,
      "confidence": 0.75,
      "confluence_status": "STRONG",
      "technical_confidence": 0.68,
      "lstm_confidence": 0.72,
      "lstm_direction": "UP",
      "alasan": "[Mode Santai] Sinyal BELI - Konfluensi: 5/6 kondisi terpenuhi..."
    }
  ],
  "rekomendasi": {
    "aksi": "BELI",
    "kekuatan": "STRONG",
    "alasan": "Technical + AI alignment bullish"
  }
}
```

### 11.7 Data Management (Legacy)

**Upload CSV:**
```http
POST /unggah-csv/?folder=BTC
Content-Type: multipart/form-data

berkas: <file.csv>
```

**Process Indicators:**
```http
POST /pra-proses/indikator/
Content-Type: application/json

{"folder": "BTC"}
```

**Backtest:**
```http
POST /sinyal/generate
Content-Type: application/json

{
  "folder": "BTC",
  "mode_trading": "santai",
  "confidence_minimum": 0.60
}
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

### 13.5 FAQ v3.0

**Q: Apa yang baru di v3.0?**
A: Multi-signal support, SPOT vs FUTURES differentiation, entry size management, active tracking dengan real-time updates, signal history, dan smart price formatting untuk small cap coins.

**Q: Bagaimana cara kerja multi-signal support?**
A: Satu symbol bisa punya maksimal 3 signals aktif bersamaan (AKTIF, SANTAI, PASIF). Sistem akan reject jika sudah ada signal OPEN untuk mode yang sama.

**Q: Apa perbedaan SPOT vs FUTURES?**
A: SPOT hanya support BELI signals dengan TP 5x ATR dan interval 1D untuk long-term investment. FUTURES support BELI/JUAL dengan TP 3x ATR dan interval sesuai mode.

**Q: Bagaimana entry size management bekerja?**
A: User set modal total dan persentase entry. Sistem calculate entry amount dalam dollar dan track P&L berdasarkan amount tersebut. Old signals tanpa entry_amount akan fallback ke modal input di Active Tracking.

**Q: Apakah auto signal service aman?**
A: Ya, service berjalan di background dan hanya monitoring. Tidak ada auto-trading, hanya auto-close signals saat hit SL/TP berdasarkan real-time price dari Binance.

**Q: Bagaimana cara backup data?**
A: Database SQLite tersimpan di `data/database/leon_engine.db`. Copy file ini untuk backup semua signals dan favorites.

**Q: Apakah bisa custom parameter trading?**
A: Saat ini parameter fixed per mode untuk konsistensi. Future update akan support custom parameters.

**Q: Kenapa confidence maksimal 80%?**
A: Sistem dirancang dengan prinsip realistic expectations. Tidak ada signal yang 100% pasti profit dalam trading.

---

## CHANGELOG v3.0

### 🚀 NEW FEATURES
- ✅ Multi-signal support per symbol (different modes)
- ✅ SPOT vs FUTURES market differentiation  
- ✅ Entry size management dengan modal & percentage
- ✅ Active signal tracking dengan real-time updates
- ✅ Signal history dengan comprehensive statistics
- ✅ Smart price formatting untuk small cap coins
- ✅ Auto signal service untuk monitoring SL/TP
- ✅ Advanced filtering system
- ✅ Live market chart dengan Binance WebSocket
- ✅ Hybrid analysis (Technical + LSTM AI)
- ✅ Cyberpunk UI dengan neon theme

### 🔧 IMPROVEMENTS
- ✅ Database schema dengan entry size columns
- ✅ Real-time P&L calculation dalam dollar
- ✅ WebSocket integration untuk live prices
- ✅ Responsive design untuk mobile
- ✅ Error handling dan user notifications
- ✅ Performance optimization
- ✅ Code restructuring dengan proper MVC

### 🐛 BUG FIXES
- ✅ Filter state preservation after auto-refresh
- ✅ Price formatting untuk decimal places
- ✅ WebSocket reconnection handling
- ✅ Memory leak prevention
- ✅ Cross-browser compatibility

---

## ROADMAP v4.0 (Future)

### 🎯 PLANNED FEATURES
- 📋 Portfolio management dengan multiple accounts
- 📋 Advanced charting dengan technical indicators overlay
- 📋 Custom parameter settings per user
- 📋 Email/Telegram notifications
- 📋 API integration dengan exchanges (Binance, Bybit)
- 📋 Advanced backtesting dengan walk-forward analysis
- 📋 Machine learning model retraining
- 📋 Multi-timeframe analysis
- 📋 Social trading features
- 📋 Mobile app (React Native)

---

*Dokumentasi Leon Liquidity Engine v3.0 CYBERPUNK*
*Advanced Cryptocurrency Trading System*
*© 2025 - Built with ❤️ for the future of trading*

**🔥 SYSTEM STATUS: FULLY OPERATIONAL**
**🚀 LAST UPDATE: December 2025**
**⚡ NEXT EVOLUTION: v4.0 QUANTUM**
