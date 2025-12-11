# MANUAL BOOK
## Leon Liquidity Engine - Sistem Cerdas Analisis Trading Cryptocurrency

---

## DAFTAR ISI

1. [Pendahuluan](#1-pendahuluan)
2. [Persyaratan Sistem](#2-persyaratan-sistem)
3. [Instalasi](#3-instalasi)
4. [Menjalankan Aplikasi](#4-menjalankan-aplikasi)
5. [Panduan Penggunaan](#5-panduan-penggunaan)
6. [Penjelasan Fitur](#6-penjelasan-fitur)
7. [Interpretasi Hasil](#7-interpretasi-hasil)
8. [Troubleshooting](#8-troubleshooting)
9. [FAQ](#9-faq)

---

## 1. PENDAHULUAN

### 1.1 Tentang Aplikasi
Leon Liquidity Engine adalah sistem cerdas berbasis web yang dirancang untuk menganalisis data historis cryptocurrency dan menghasilkan sinyal trading (BELI/JUAL) berdasarkan indikator teknikal.

### 1.2 Fitur Utama
- ✅ Upload dan manajemen data CSV
- ✅ Preprocessing otomatis dengan indikator teknikal
- ✅ Generate sinyal trading dengan 3 mode (Aktif, Santai, Pasif)
- ✅ Confidence scoring untuk setiap sinyal
- ✅ Backtesting otomatis dengan statistik performa
- ✅ Dashboard interaktif untuk monitoring

### 1.3 Komponen Sistem Cerdas
| Komponen | Deskripsi |
|----------|-----------|
| Knowledge Base | Aturan trading dari expert (RSI, EMA, S/R, Divergence) |
| Inference Engine | Mesin inferensi untuk generate sinyal |
| Confidence Scoring | Perhitungan tingkat kepercayaan sinyal |
| Backtesting Engine | Simulasi dan validasi performa |

---

## 2. PERSYARATAN SISTEM

### 2.1 Hardware Minimum
- Processor: Intel Core i3 atau setara
- RAM: 4 GB
- Storage: 500 MB free space
- Koneksi internet (untuk instalasi dependencies)

### 2.2 Software Requirements
- Operating System: Windows 10/11, macOS, atau Linux
- Python: Versi 3.8 atau lebih baru
- Web Browser: Chrome, Firefox, Edge (versi terbaru)

### 2.3 Python Dependencies
```
fastapi>=0.100.0
uvicorn>=0.23.0
pandas>=2.0.0
numpy>=1.24.0
python-multipart>=0.0.6
```

---

## 3. INSTALASI

### 3.1 Clone/Download Project
```bash
# Jika menggunakan Git
git clone <repository-url>
cd leon-liquidity-engine

# Atau extract file ZIP ke folder yang diinginkan
```

### 3.2 Buat Virtual Environment (Opsional tapi Disarankan)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3.3 Install Dependencies
```bash
pip install -r requirements.txt
```

### 3.4 Verifikasi Instalasi
```bash
python -c "import fastapi; import pandas; print('Instalasi berhasil!')"
```

---

## 4. MENJALANKAN APLIKASI

### 4.1 Start Server
```bash
# Dari root folder project
python -m uvicorn backend.app:app --reload --port 8000
```

### 4.2 Akses Aplikasi
Buka web browser dan akses:
```
http://127.0.0.1:8000
```

### 4.3 Stop Server
Tekan `Ctrl + C` di terminal untuk menghentikan server.

---

## 5. PANDUAN PENGGUNAAN

### 5.1 Halaman Dashboard

Dashboard adalah halaman utama yang menampilkan ringkasan statistik sistem.

**Informasi yang Ditampilkan:**
- Total Folder (coin pairs)
- Total File CSV
- Total File Processed
- Total Sinyal yang dihasilkan
- Statistik Backtest (Win Rate, Avg P&L, Duration)
- Breakdown sinyal per mode trading

**Screenshot Area:**
```
┌─────────────────────────────────────────────────────────────┐
│  DASHBOARD                                                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│  │ Folders  │ │  Files   │ │Processed │ │ Signals  │       │
│  │    10    │ │   150    │ │   150    │ │   45     │       │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘       │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  BACKTEST PERFORMANCE                                │   │
│  │  Win Rate: 85.2%  |  Avg P&L: +2.15%  |  Duration: 24h│  │
│  │  HIT_TP: 35  |  HIT_SL: 6  |  TIMEOUT: 4             │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 5.2 Manajemen Folder

**Langkah-langkah:**

1. **Buat Folder Baru**
   - Klik tombol "Buat Folder"
   - Masukkan nama folder (contoh: BTC, ETH, SOL)
   - Klik "Simpan"

2. **Rename Folder**
   - Klik ikon pensil di samping nama folder
   - Masukkan nama baru
   - Klik "Simpan"

3. **Hapus Folder**
   - Klik ikon tempat sampah di samping nama folder
   - Konfirmasi penghapusan

**Tips:** Gunakan nama coin pair sebagai nama folder (contoh: BTC, ETH, BNB)

### 5.3 Upload Data CSV

**Format Data yang Diterima:**
Data harus dalam format CSV dengan kolom berikut:
```
open_time,open,high,low,close,volume
1704326400000,42000.5,42500.0,41800.0,42300.0,1500.5
1704330000000,42300.0,42800.0,42100.0,42600.0,1800.2
...
```

**Langkah-langkah:**
1. Pilih folder tujuan dari dropdown
2. Klik "Pilih File" atau drag & drop file CSV
3. Klik "Upload"
4. Tunggu hingga proses selesai
5. Cek status upload di bagian bawah

**Sumber Data:**
- Binance Vision: https://data.binance.vision/
- Download data kline/spot dengan interval 1h (1 jam)

### 5.4 Proses Indikator

Setelah upload data, lakukan preprocessing untuk menambahkan indikator teknikal.

**Langkah-langkah:**
1. Pilih folder yang akan diproses
2. Klik "Proses Indikator"
3. Tunggu hingga proses selesai

**Indikator yang Ditambahkan:**
| Indikator | Periode | Fungsi |
|-----------|---------|--------|
| RSI | 6, 8, 10, 14 | Mengukur momentum |
| EMA | 9, 20, 50, 200 | Mengukur trend |
| ATR | 14 | Mengukur volatilitas |

### 5.5 Generate Sinyal Trading

**Langkah-langkah:**
1. Pilih folder yang sudah diproses
2. Pilih mode trading:
   - **Aktif**: Untuk trading jangka pendek (1-4 jam)
   - **Santai**: Untuk trading menengah (4-12 jam)
   - **Pasif**: Untuk swing trading (12 jam - 3 hari)
3. Klik "Generate Sinyal"
4. Tunggu hingga proses selesai
5. Lihat hasil di tabel sinyal

**Penjelasan Mode Trading:**

| Mode | RSI Period | RSI Threshold | Target Durasi | Risk-Reward |
|------|------------|---------------|---------------|-------------|
| Aktif | 6 | 15/85 | 1-4 jam | 2.0 |
| Santai | 8 | 18/82 | 4-12 jam | 2.5 |
| Pasif | 14 | 15/85 | 12h - 3 hari | 3.0 |

---

## 6. PENJELASAN FITUR

### 6.1 Sistem Confidence Scoring

Confidence adalah tingkat kepercayaan sistem terhadap sinyal yang dihasilkan.

**Komponen Perhitungan:**
```
Confidence = Base (35%) + Bonus Confluence + Bonus Divergence + Bonus S/R

Dimana:
- Bonus Confluence: 8% - 20% (berdasarkan jumlah kondisi terpenuhi)
- Bonus Divergence: 12% (jika ada divergence)
- Bonus S/R: 5% - 15% (berdasarkan jarak ke Support/Resistance)

Range: 35% - 80%
```

**Interpretasi Confidence:**
| Range | Kategori | Rekomendasi |
|-------|----------|-------------|
| 70% - 80% | Tinggi | Sinyal sangat kuat, layak dipertimbangkan |
| 60% - 70% | Sedang | Sinyal cukup kuat, perlu konfirmasi tambahan |
| < 60% | Rendah | Sinyal lemah, sebaiknya diabaikan |

### 6.2 Sistem Backtesting

Backtesting adalah simulasi trading menggunakan data historis untuk mengukur performa sinyal.

**Hasil Backtest:**
| Status | Deskripsi |
|--------|-----------|
| HIT_TP | Sinyal mencapai Take Profit (profit) |
| HIT_SL | Sinyal mencapai Stop Loss (loss) |
| TIMEOUT | Sinyal tidak mencapai TP/SL dalam 168 jam |

**Statistik yang Dihitung:**
- **Win Rate**: Persentase sinyal yang profit (HIT_TP / Total Closed)
- **Avg P&L**: Rata-rata profit/loss per sinyal
- **Avg Duration**: Rata-rata durasi sinyal (dalam jam)
- **Avg Profit**: Rata-rata profit untuk sinyal yang profit
- **Avg Loss**: Rata-rata loss untuk sinyal yang loss

### 6.3 Indikator Teknikal

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
- Dideteksi dari pivot points historis

**Divergence**
- Bullish Divergence: Harga turun tapi RSI naik (sinyal reversal naik)
- Bearish Divergence: Harga naik tapi RSI turun (sinyal reversal turun)

---

## 7. INTERPRETASI HASIL

### 7.1 Membaca Tabel Sinyal

```
┌──────────┬──────┬──────────┬──────────┬──────────┬────────┬─────────┬───────┐
│   Pair   │ Tipe │  Entry   │    SL    │    TP    │ Conf.  │ Result  │  P&L  │
├──────────┼──────┼──────────┼──────────┼──────────┼────────┼─────────┼───────┤
│ BTCUSDT  │ BELI │ 97992.00 │ 97340.76 │ 99620.09 │  65%   │ HIT_TP  │+2.15% │
│ BTCUSDT  │ JUAL │ 98910.00 │ 99969.07 │ 96262.33 │  60%   │ HIT_SL  │-1.07% │
└──────────┴──────┴──────────┴──────────┴──────────┴────────┴─────────┴───────┘
```

**Penjelasan Kolom:**
- **Pair**: Pasangan mata uang (contoh: BTCUSDT)
- **Tipe**: Jenis sinyal (BELI = Long, JUAL = Short)
- **Entry**: Harga masuk posisi
- **SL**: Stop Loss (batas kerugian)
- **TP**: Take Profit (target keuntungan)
- **Conf.**: Confidence score (tingkat kepercayaan)
- **Result**: Hasil backtest (HIT_TP/HIT_SL/TIMEOUT)
- **P&L**: Profit/Loss dalam persentase

### 7.2 Membaca Statistik Backtest

```
Win Rate: 85.2%    → 85.2% sinyal menghasilkan profit
Avg P&L: +2.15%    → Rata-rata profit per sinyal adalah 2.15%
Duration: 24h      → Rata-rata sinyal selesai dalam 24 jam
HIT_TP: 35         → 35 sinyal mencapai Take Profit
HIT_SL: 6          → 6 sinyal mencapai Stop Loss
TIMEOUT: 4         → 4 sinyal tidak selesai dalam 168 jam
```

### 7.3 Rekomendasi Penggunaan

**Untuk Pemula:**
- Gunakan mode **Santai** (lebih seimbang)
- Fokus pada sinyal dengan confidence >= 65%
- Perhatikan win rate minimal 70%

**Untuk Intermediate:**
- Gunakan mode **Aktif** untuk trading lebih sering
- Kombinasikan dengan analisis manual
- Perhatikan alasan sinyal untuk pembelajaran

**Untuk Advanced:**
- Gunakan mode **Pasif** untuk swing trading
- Analisis divergence untuk konfirmasi tambahan
- Sesuaikan parameter sesuai kondisi pasar

---

## 8. TROUBLESHOOTING

### 8.1 Server Tidak Bisa Start

**Masalah:** Error saat menjalankan `uvicorn`

**Solusi:**
```bash
# Pastikan dependencies terinstall
pip install -r requirements.txt

# Pastikan berada di folder yang benar
cd path/to/leon-liquidity-engine

# Coba jalankan ulang
python -m uvicorn backend.app:app --reload --port 8000
```

### 8.2 Upload CSV Gagal

**Masalah:** File CSV tidak bisa diupload

**Solusi:**
1. Pastikan format file adalah .csv
2. Pastikan kolom sesuai: open_time, open, high, low, close, volume
3. Pastikan tidak ada karakter khusus di nama file
4. Pastikan folder tujuan sudah dibuat

### 8.3 Tidak Ada Sinyal yang Dihasilkan

**Masalah:** Generate sinyal menghasilkan 0 sinyal

**Solusi:**
1. Pastikan data sudah diproses dengan indikator
2. Coba mode trading yang berbeda
3. Pastikan data memiliki minimal 10 baris
4. Cek apakah data memiliki variasi harga yang cukup

### 8.4 Dashboard Tidak Menampilkan Data

**Masalah:** Statistik backtest menampilkan "-" atau "0"

**Solusi:**
1. Hard refresh browser (Ctrl+Shift+R)
2. Generate sinyal terlebih dahulu
3. Pindah ke halaman Dashboard
4. Cek browser console (F12) untuk error

---

## 9. FAQ

### Q1: Apakah sistem ini bisa digunakan untuk trading real?
**A:** Sistem ini dirancang sebagai alat bantu analisis dan pembelajaran. Untuk trading real, selalu lakukan analisis tambahan dan manajemen risiko yang tepat.

### Q2: Berapa akurasi sistem ini?
**A:** Berdasarkan backtesting, sistem mencapai win rate 70-90% tergantung mode trading dan kondisi pasar. Namun, performa masa lalu tidak menjamin hasil di masa depan.

### Q3: Data dari mana yang bisa digunakan?
**A:** Sistem menerima data OHLCV dalam format CSV. Sumber yang direkomendasikan adalah Binance Vision (data.binance.vision) dengan interval 1 jam (1h).

### Q4: Apa perbedaan mode Aktif, Santai, dan Pasif?
**A:** 
- **Aktif**: Trading cepat (1-4 jam), RSI lebih sensitif
- **Santai**: Trading menengah (4-12 jam), seimbang
- **Pasif**: Swing trading (12h-3 hari), lebih konservatif

### Q5: Mengapa confidence tidak pernah mencapai 100%?
**A:** Sistem dirancang dengan prinsip kejujuran. Tidak ada sinyal yang 100% pasti profit. Range confidence 35-80% mencerminkan realitas trading.

### Q6: Bagaimana cara meningkatkan win rate?
**A:** 
- Fokus pada sinyal dengan confidence tinggi (>= 70%)
- Gunakan mode yang sesuai dengan gaya trading
- Pastikan data yang digunakan berkualitas

---

## LAMPIRAN

### A. Struktur Folder Project
```
leon-liquidity-engine/
├── backend/
│   ├── api/
│   ├── core/
│   ├── models/
│   ├── services/
│   │   ├── generator_sinyal_unified.py
│   │   ├── praproses_data.py
│   │   └── backtesting_engine.py
│   ├── utils/
│   └── app.py
├── data/
│   ├── uploads/
│   └── processed/
├── docs/
│   ├── DESAIN_PERANCANGAN.md
│   ├── MANUAL_BOOK.md
│   └── PANDUAN_LENGKAP.md
├── frontend/
│   └── index.html
├── tests/
├── requirements.txt
└── README.md
```

### B. API Endpoints
| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| GET | / | Halaman utama (Dashboard) |
| GET | /cek-kesehatan | Health check |
| GET | /folder/daftar | Daftar semua folder |
| POST | /folder/buat | Buat folder baru |
| PUT | /folder/rename | Rename folder |
| DELETE | /folder/hapus | Hapus folder |
| POST | /unggah-csv/ | Upload file CSV |
| GET | /unggah-csv/daftar | Daftar file di folder |
| DELETE | /unggah-csv/hapus | Hapus file |
| POST | /pra-proses/indikator/ | Proses indikator |
| POST | /sinyal/generate | Generate sinyal trading |

### C. Referensi
1. RSI (Relative Strength Index) - J. Welles Wilder Jr.
2. EMA (Exponential Moving Average) - Technical Analysis
3. ATR (Average True Range) - J. Welles Wilder Jr.
4. Support/Resistance - Price Action Analysis
5. Divergence - Momentum Analysis

---

*Manual Book Leon Liquidity Engine v1.0*
*Sistem Cerdas untuk Analisis Trading Cryptocurrency*
