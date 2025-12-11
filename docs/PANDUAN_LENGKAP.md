# Panduan Lengkap Generator Sinyal Trading

## 📚 Daftar Isi

1. [Instalasi dan Setup](#instalasi-dan-setup)
2. [Struktur Project](#struktur-project)
3. [Mode Trading](#mode-trading)
4. [SISTEM DELTA](#sistem-delta)
5. [API Reference](#api-reference)
6. [Troubleshooting](#troubleshooting)

## 🚀 Instalasi dan Setup

### Persyaratan Sistem
- Python 3.11+ (Recommended: 3.13)
- RAM minimal 4GB
- Storage 2GB+ untuk data H1 2022-2025

### Langkah Instalasi
```bash
# 1. Clone repository
git clone <repository-url>
cd indikator

# 2. Install dependencies
pip install -r requirements.txt

# 3. Jalankan server
python -m uvicorn backend.app:app --reload --port 8000

# 4. Akses aplikasi
# Browser: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

## 📁 Struktur Project

```
indikator/
├── backend/                    # Backend API
│   ├── api/                   # API endpoints (future)
│   ├── core/                  # Konfigurasi inti
│   ├── models/                # Database models (future)
│   ├── services/              # Business logic
│   │   ├── praproses_data.py     # Data preprocessing
│   │   ├── generator_sinyal.py   # Signal generator legacy
│   │   └── generator_sinyal_delta.py # Advanced DELTA system
│   ├── utils/                 # Helper functions (future)
│   └── app.py                 # Main FastAPI application
├── frontend/                   # Web interface
│   └── index.html             # Dashboard UI
├── data/                      # Data storage
│   ├── uploads/              # Raw CSV files
│   └── processed/            # Processed data with indicators
├── tests/                     # Test suite (future)
├── docs/                      # Dokumentasi
│   └── PANDUAN_LENGKAP.md    # File ini
└── requirements.txt           # Python dependencies
```

## 🎯 Mode Trading

### Cepat (1-4 Jam) - H1 Data
**Karakteristik:**
- Timeframe: 1-4 jam (H1 candles)
- RSI Period: 6, 8 (sensitif untuk H1)
- EMA: 9, 20, 50
- Target: 20-50 sinyal per hari
- Risk/Reward: 1.5:1
- ATR Multiplier: 0.5 (SL moderate)

**Cocok untuk:**
- Active trading dengan H1 data
- Quick trend catching
- Moderate risk tolerance

### Intraday (4-12 Jam) - H1 Data
**Karakteristik:**
- Timeframe: 4-12 jam (H1 candles)
- RSI Period: 10 (dengan smoothing MA3)
- EMA: 20, 50, 200
- Target: 5-15 sinyal per hari
- Risk/Reward: 2:1
- ATR Multiplier: 0.7 (SL balanced)

**Cocok untuk:**
- Day trading dengan H1 precision
- Trend following
- Work-life balance

### Swing (12 Jam - 3 Hari) - H1 Data
**Karakteristik:**
- Timeframe: 12 jam - 3 hari (H1 candles)
- RSI Period: 14 (standar)
- EMA: 50, 100, 200 (longer periods untuk H1)
- Target: 2-8 sinyal per hari
- Risk/Reward: 3:1
- ATR Multiplier: 1.0 (SL lebar)

**Cocok untuk:**
- Position trading dengan H1 accuracy
- Multi-day trend analysis
- Conservative trading

## 🔥 SISTEM DELTA

### Keunggulan vs Sistem Legacy

| Feature | Legacy | SISTEM DELTA |
|---------|--------|--------------|
| Confluence Required | 4/6 (66%) | 3/6 (50%) |
| Divergence | WAJIB | OPSIONAL |
| S/R Distance | <1% | <2% |
| Confidence Scoring | ❌ | ✅ 50-95% |
| User Control | ❌ | ✅ |
| Signal Frequency | Rendah | Tinggi |

### Algoritma Confidence Scoring

```python
# Base confidence
confidence_base = 40%

# Confluence bonus
if confluence_count == 3: +10%
if confluence_count == 4: +15%
if confluence_count == 5: +20%
if confluence_count == 6: +25%

# Feature bonuses
+ Divergence detected: +15%
+ Near Support/Resistance: +5% to +15%
+ Strong volume: +5% to +10%
+ EMA slope strength: +5% to +10%
+ RSI momentum: +5% to +10%

# Final range: 50-95%
```

### Confluence Indicators (6 total)

1. **EMA Alignment**: Trend direction consistency
2. **EMA Slope**: Trend strength
3. **RSI Breakout**: Momentum confirmation
4. **Candle Pattern**: Price action strength
5. **Trend Direction**: Multi-timeframe alignment
6. **Support/Resistance**: Key level proximity

## 📊 API Reference

### Upload CSV
```http
POST /unggah-csv/
Content-Type: multipart/form-data

Parameters:
- berkas: CSV file (Binance format)
- folder: Target folder name
```

### Preprocessing
```http
POST /pra-proses/indikator/
Content-Type: application/json

{
  "folder": "BTC"
}
```

### Generate Signals
```http
POST /sinyal/generate
Content-Type: application/json

{
  "folder": "BTC",
  "mode_trading": "scalping",
  "confidence_minimum": 0.60,
  "gunakan_delta": true,
  "rsi_oversold": 30,
  "rsi_overbought": 70,
  "rasio_risk_reward": 2.0
}
```

### Response Format
```json
{
  "jumlah_sinyal": 124,
  "sistem": "DELTA (Akurasi Tinggi)",
  "statistik_confidence": {
    "rata_rata": 0.8272,
    "terendah": 0.60,
    "tertinggi": 0.95
  },
  "sinyal": [
    {
      "tipe": "BUY",
      "entry": 67234.5,
      "stop_loss": 66890.2,
      "take_profit": 68012.8,
      "confidence": 0.75,
      "alasan": "RSI breakout + EMA cross + divergence",
      "timestamp": "2024-01-01T10:30:00",
      "pair": "BTCUSDT"
    }
  ]
}
```

## 🔧 Troubleshooting

### Tidak Ada Sinyal?

**Kemungkinan Penyebab:**
1. Data tidak cukup (butuh minimal 1 hari untuk Scalping)
2. Confidence threshold terlalu tinggi
3. Market kondisi sideways (normal)

**Solusi:**
```python
# Turunkan confidence minimum
confidence_minimum = 0.50

# Check data adequacy
# Scalping: minimal 1 hari (1,440 candles M1)
# Intraday: minimal 3-7 hari
# Swing: minimal 7-30 hari
```

### Error saat Generate?

**Kemungkinan Penyebab:**
1. CSV format salah
2. Belum menjalankan preprocessing
3. Import path error setelah restructure

**Solusi:**
```bash
# 1. Check CSV format (harus Binance OHLCV)
# 2. Jalankan preprocessing dulu
# 3. Restart server setelah restructure
python -m uvicorn backend.app:app --reload --port 8000
```

### Performance Issues?

**Optimasi:**
```python
# 1. Gunakan data yang sudah diproses
# 2. Batasi timeframe analysis
# 3. Increase confidence threshold untuk reduce signals
confidence_minimum = 0.70  # Less signals, higher quality
```

## 📈 Best Practices

### Data Management
- Gunakan data H1 untuk performa optimal
- Preprocessing sekali, pakai berkali-kali
- Backup data processed secara berkala

### Signal Selection
- Scalping: confidence >= 70% untuk akurasi tinggi
- Intraday: confidence >= 60% untuk balance
- Swing: confidence >= 65% untuk quality

### Risk Management
- Selalu gunakan Stop Loss dari sistem
- Take Profit bisa disesuaikan dengan market condition
- Monitor confidence score untuk filter sinyal

---

**Dokumentasi ini akan terus diupdate seiring pengembangan sistem.**