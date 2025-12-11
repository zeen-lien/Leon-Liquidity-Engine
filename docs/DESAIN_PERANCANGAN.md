# DESAIN PERANCANGAN SISTEM
## Leon Liquidity Engine - Sistem Cerdas untuk Analisis Trading Cryptocurrency

---

## 1. PENDAHULUAN

### 1.1 Latar Belakang
Trading cryptocurrency memerlukan analisis teknikal yang kompleks dan pengambilan keputusan yang cepat. Trader pemula sering kesulitan mengidentifikasi waktu yang tepat untuk membeli atau menjual aset. Sistem cerdas ini dirancang untuk membantu trader dengan menganalisis data historis dan memberikan rekomendasi sinyal trading berdasarkan indikator teknikal.

### 1.2 Tujuan Sistem
1. Menganalisis data historis cryptocurrency secara otomatis
2. Mengidentifikasi peluang trading berdasarkan indikator teknikal
3. Memberikan rekomendasi sinyal BELI/JUAL dengan tingkat kepercayaan (confidence)
4. Melakukan backtesting untuk validasi performa sistem

### 1.3 Ruang Lingkup
- Input: Data OHLCV (Open, High, Low, Close, Volume) cryptocurrency
- Proses: Analisis teknikal dengan multiple indicators
- Output: Sinyal trading dengan confidence score dan hasil backtest

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
│  │   (UI/UX)    │◄──►│   (FastAPI)  │◄──►│   (Trading Rules)    │   │
│  └──────────────┘    └──────────────┘    └──────────────────────┘   │
│         │                   │                       │                │
│         ▼                   ▼                       ▼                │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────────────┐   │
│  │  Dashboard   │    │  Praproses   │    │  Expert Rules:       │   │
│  │  Upload CSV  │    │  Data        │    │  - RSI Extreme       │   │
│  │  Generate    │    │  (Indikator) │    │  - EMA Alignment     │   │
│  │  Sinyal      │    │              │    │  - Trend Filter      │   │
│  └──────────────┘    └──────────────┘    │  - S/R Detection     │   │
│                             │            │  - Divergence        │   │
│                             ▼            └──────────────────────┘   │
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
│                             │                                        │
│                             ▼                                        │
│                      ┌──────────────┐                               │
│                      │  BACKTEST    │                               │
│                      │   ENGINE     │                               │
│                      │              │                               │
│                      │ Win Rate,    │                               │
│                      │ P&L, Stats   │                               │
│                      └──────────────┘                               │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### 2.2 Komponen Sistem Cerdas

#### A. Knowledge Base (Basis Pengetahuan)
Berisi aturan-aturan trading dari expert yang dikodekan dalam sistem:

| No | Aturan | Deskripsi |
|----|--------|-----------|
| 1 | RSI Oversold | RSI <= 15 (extreme) menandakan jenuh jual |
| 2 | RSI Overbought | RSI >= 85 (extreme) menandakan jenuh beli |
| 3 | EMA Alignment | EMA Fast > EMA Mid = trend naik |
| 4 | Trend Filter | Harga > EMA200 = uptrend, < EMA200 = downtrend |
| 5 | Support/Resistance | Deteksi level S/R dari pivot points |
| 6 | Divergence | Harga vs RSI divergence = reversal signal |

#### B. Inference Engine (Mesin Inferensi)
Proses pengambilan keputusan berdasarkan aturan:

```
INPUT: Data OHLCV + Indikator Teknikal
         │
         ▼
┌─────────────────────────────────────┐
│     CEK KONDISI (6 ATURAN)          │
│                                     │
│  1. RSI Oversold/Overbought? ──────►│
│  2. EMA Alignment? ────────────────►│
│  3. Price vs EMA Fast? ────────────►│
│  4. Trend Filter EMA200? ──────────►│
│  5. Dekat Support/Resistance? ─────►│
│  6. Candle Bullish/Bearish? ───────►│
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

#### C. Decision Support System
Sistem memberikan rekomendasi dengan informasi lengkap:
- Tipe sinyal (BELI/JUAL)
- Entry price
- Stop Loss (batas kerugian)
- Take Profit (target keuntungan)
- Confidence score (tingkat kepercayaan)
- Alasan (penjelasan mengapa sinyal dihasilkan)

---

## 3. DESAIN DATABASE

### 3.1 Struktur Data Input (CSV)

| Kolom | Tipe Data | Deskripsi |
|-------|-----------|-----------|
| open_time | datetime | Waktu pembukaan candle |
| open | float | Harga pembukaan |
| high | float | Harga tertinggi |
| low | float | Harga terendah |
| close | float | Harga penutupan |
| volume | float | Volume transaksi |

### 3.2 Struktur Data Processed (Dengan Indikator)

| Kolom | Tipe Data | Deskripsi |
|-------|-----------|-----------|
| rsi_6 | float | RSI periode 6 (Mode Aktif) |
| rsi_8 | float | RSI periode 8 (Mode Santai) |
| rsi_14 | float | RSI periode 14 (Mode Pasif) |
| ema_9 | float | EMA periode 9 |
| ema_20 | float | EMA periode 20 |
| ema_50 | float | EMA periode 50 |
| ema_200 | float | EMA periode 200 |
| atr_14 | float | Average True Range |

### 3.3 Struktur Output Sinyal

```json
{
  "tipe": "BELI",
  "entry": 97992.0,
  "stop_loss": 97340.76,
  "take_profit": 99620.09,
  "confidence": 0.65,
  "alasan": "[Mode Santai Expert] Sinyal BELI, Konfluensi: 5/6, EMA sejajar naik, dekat Support (0.6%).",
  "timestamp": "2025-01-04T14:00:00",
  "pair": "BTCUSDT",
  "backtest_result": "HIT_TP",
  "pnl_percent": 2.15
}
```

---

## 4. ALGORITMA SISTEM CERDAS

### 4.1 Algoritma Deteksi Sinyal

```python
ALGORITMA: Generate_Sinyal_Trading

INPUT:
  - df: DataFrame dengan data OHLCV + indikator
  - config: Konfigurasi mode trading
  - confidence_minimum: Threshold minimum

OUTPUT:
  - sinyal: Object SinyalTrading atau None

PROSES:
1. AMBIL data baris terakhir dari df
2. HITUNG nilai indikator (RSI, EMA, ATR)

3. CEK kondisi BELI:
   a. kondisi_rsi = (RSI <= threshold_oversold)
   b. kondisi_ema = (EMA_fast > EMA_mid)
   c. kondisi_price = (close > EMA_fast)
   d. kondisi_trend = (close > EMA_200)
   e. kondisi_sr = (jarak_ke_support < 2%)
   f. kondisi_candle = (close > open)

4. HITUNG confluence:
   jumlah_confluence = SUM(kondisi_a sampai kondisi_f)

5. JIKA jumlah_confluence >= 4:
   a. HITUNG confidence dengan formula:
      - base = 0.35
      - bonus_confluence = f(jumlah_confluence)
      - bonus_divergence = 0.12 jika ada divergence
      - bonus_sr = f(jarak_ke_support)
      - confidence = MIN(0.80, base + semua_bonus)
   
   b. JIKA confidence >= confidence_minimum:
      - HITUNG stop_loss dari support atau ATR
      - HITUNG take_profit dari risk-reward ratio
      - RETURN SinyalTrading(BELI, entry, sl, tp, confidence)

6. CEK kondisi JUAL (mirror dari kondisi BELI)

7. RETURN None jika tidak ada sinyal
```

### 4.2 Algoritma Confidence Scoring

```python
ALGORITMA: Hitung_Confidence_Jujur

INPUT:
  - jumlah_confluence: int (0-6)
  - total_kondisi: int (6)
  - ada_divergence: bool
  - jarak_support_persen: float
  - tipe_sinyal: string

OUTPUT:
  - confidence: float (0.35 - 0.80)

PROSES:
1. SET confidence = 0.35 (base conservative)

2. HITUNG rasio_confluence = jumlah_confluence / total_kondisi

3. TAMBAH bonus confluence:
   - JIKA rasio >= 1.0 (6/6): confidence += 0.20
   - JIKA rasio >= 0.83 (5/6): confidence += 0.15
   - JIKA rasio >= 0.67 (4/6): confidence += 0.12
   - JIKA rasio >= 0.50 (3/6): confidence += 0.08

4. JIKA ada_divergence:
   confidence += 0.12

5. JIKA tipe_sinyal == "BELI" DAN jarak_support_persen != None:
   - JIKA jarak < 0.5%: confidence += 0.15
   - JIKA jarak < 1.0%: confidence += 0.10
   - JIKA jarak < 2.0%: confidence += 0.08

6. RETURN MIN(0.80, confidence)
```

### 4.3 Algoritma Backtesting

```python
ALGORITMA: Backtest_Sinyal

INPUT:
  - sinyal: Object dengan entry, sl, tp, confidence
  - future_data: DataFrame data setelah entry

OUTPUT:
  - result: "HIT_TP" | "HIT_SL" | "TIMEOUT"
  - pnl_percent: float
  - duration: int (jam)

PROSES:
1. UNTUK setiap candle di future_data (max 168 jam):
   
   2. JIKA sinyal.tipe == "BELI":
      a. JIKA high >= take_profit:
         - pnl = ((tp - entry) / entry) * 100
         - RETURN ("HIT_TP", pnl, jam)
      b. JIKA low <= stop_loss:
         - pnl = ((sl - entry) / entry) * 100
         - RETURN ("HIT_SL", pnl, jam)
   
   3. JIKA sinyal.tipe == "JUAL":
      a. JIKA low <= take_profit:
         - pnl = ((entry - tp) / entry) * 100
         - RETURN ("HIT_TP", pnl, jam)
      b. JIKA high >= stop_loss:
         - pnl = ((entry - sl) / entry) * 100
         - RETURN ("HIT_SL", pnl, jam)

4. RETURN ("TIMEOUT", 0, 168)
```

---

## 5. FLOWCHART SISTEM

### 5.1 Flowchart Utama

```
                    ┌─────────────┐
                    │   START     │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │ Upload CSV  │
                    │ Data OHLCV  │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │ Validasi    │
                    │ Format Data │
                    └──────┬──────┘
                           │
                    ┌──────┴──────┐
                    │             │
                    ▼             ▼
              ┌─────────┐   ┌─────────┐
              │  Valid  │   │ Invalid │
              └────┬────┘   └────┬────┘
                   │             │
                   │             ▼
                   │       ┌─────────┐
                   │       │  Error  │
                   │       │ Message │
                   │       └────┬────┘
                   │             │
                   ▼             │
            ┌─────────────┐      │
            │ Pra-proses  │      │
            │ Tambah      │      │
            │ Indikator   │      │
            └──────┬──────┘      │
                   │             │
                   ▼             │
            ┌─────────────┐      │
            │ Pilih Mode  │      │
            │ Trading     │      │
            └──────┬──────┘      │
                   │             │
                   ▼             │
            ┌─────────────┐      │
            │ Generate    │      │
            │ Sinyal      │      │
            └──────┬──────┘      │
                   │             │
                   ▼             │
            ┌─────────────┐      │
            │ Backtest    │      │
            │ Sinyal      │      │
            └──────┬──────┘      │
                   │             │
                   ▼             │
            ┌─────────────┐      │
            │ Tampilkan   │◄─────┘
            │ Hasil       │
            └──────┬──────┘
                   │
                   ▼
            ┌─────────────┐
            │    END      │
            └─────────────┘
```

### 5.2 Flowchart Inference Engine

```
                    ┌─────────────┐
                    │ Data Candle │
                    │ + Indikator │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │ Cek Market  │
                    │ Regime      │
                    └──────┬──────┘
                           │
                    ┌──────┴──────┐
                    │             │
                    ▼             ▼
              ┌─────────┐   ┌─────────┐
              │ Choppy  │   │ Trending│
              │ (Skip)  │   │ (Lanjut)│
              └────┬────┘   └────┬────┘
                   │             │
                   ▼             ▼
              ┌─────────┐   ┌─────────────┐
              │  None   │   │ Cek 6       │
              └─────────┘   │ Kondisi     │
                            └──────┬──────┘
                                   │
                                   ▼
                            ┌─────────────┐
                            │ Confluence  │
                            │ >= 4/6 ?    │
                            └──────┬──────┘
                                   │
                            ┌──────┴──────┐
                            │             │
                            ▼             ▼
                      ┌─────────┐   ┌─────────┐
                      │   Ya    │   │  Tidak  │
                      └────┬────┘   └────┬────┘
                           │             │
                           ▼             ▼
                    ┌─────────────┐ ┌─────────┐
                    │ Hitung      │ │  None   │
                    │ Confidence  │ └─────────┘
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │ Confidence  │
                    │ >= Min ?    │
                    └──────┬──────┘
                           │
                    ┌──────┴──────┐
                    │             │
                    ▼             ▼
              ┌─────────┐   ┌─────────┐
              │   Ya    │   │  Tidak  │
              └────┬────┘   └────┬────┘
                   │             │
                   ▼             ▼
            ┌─────────────┐ ┌─────────┐
            │ Generate    │ │  None   │
            │ Sinyal      │ └─────────┘
            │ BELI/JUAL   │
            └─────────────┘
```

---

## 6. USE CASE DIAGRAM

```
                    ┌─────────────────────────────────────┐
                    │     LEON LIQUIDITY ENGINE           │
                    │                                     │
    ┌───────┐       │  ┌─────────────────────────────┐   │
    │       │       │  │                             │   │
    │ User  │───────┼─►│  UC1: Upload Data CSV       │   │
    │       │       │  │                             │   │
    └───────┘       │  └─────────────────────────────┘   │
        │           │                                     │
        │           │  ┌─────────────────────────────┐   │
        │           │  │                             │   │
        ├───────────┼─►│  UC2: Kelola Folder         │   │
        │           │  │                             │   │
        │           │  └─────────────────────────────┘   │
        │           │                                     │
        │           │  ┌─────────────────────────────┐   │
        │           │  │                             │   │
        ├───────────┼─►│  UC3: Proses Indikator      │   │
        │           │  │                             │   │
        │           │  └─────────────────────────────┘   │
        │           │                                     │
        │           │  ┌─────────────────────────────┐   │
        │           │  │                             │   │
        ├───────────┼─►│  UC4: Generate Sinyal       │   │
        │           │  │                             │   │
        │           │  └─────────────────────────────┘   │
        │           │                                     │
        │           │  ┌─────────────────────────────┐   │
        │           │  │                             │   │
        └───────────┼─►│  UC5: Lihat Dashboard       │   │
                    │  │                             │   │
                    │  └─────────────────────────────┘   │
                    │                                     │
                    └─────────────────────────────────────┘
```

---

## 7. TEKNOLOGI YANG DIGUNAKAN

| Komponen | Teknologi | Fungsi |
|----------|-----------|--------|
| Backend | Python 3.x | Bahasa pemrograman utama |
| Framework | FastAPI | REST API framework |
| Data Processing | Pandas | Manipulasi data tabular |
| Numerical | NumPy | Komputasi numerik |
| Frontend | HTML/CSS/JS | User interface |
| Server | Uvicorn | ASGI server |

---

## 8. KESIMPULAN

Leon Liquidity Engine adalah implementasi **Sistem Cerdas** yang menggabungkan:

1. **Rule-Based Expert System** - Aturan trading dari expert dikodekan dalam sistem
2. **Inference Engine** - Mesin inferensi untuk pengambilan keputusan
3. **Decision Support System** - Memberikan rekomendasi dengan confidence score
4. **Probabilistic Reasoning** - Perhitungan confidence berdasarkan multiple factors
5. **Simulation & Validation** - Backtesting untuk validasi performa

Sistem ini membantu trader dalam menganalisis pasar cryptocurrency dan memberikan rekomendasi trading yang terukur dan dapat dipertanggungjawabkan.

---

*Dokumen ini dibuat sebagai bagian dari tugas Sistem Cerdas*
*Leon Liquidity Engine v1.0*
