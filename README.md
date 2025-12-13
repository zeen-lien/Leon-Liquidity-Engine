# Leon Liquidity Engine v3.0

Trading Signal Generator dengan AI Prediction untuk **Spot & Futures** market.

## Fitur Utama

### Live Trading
- **Dashboard** - Command center dengan watchlist, quick signal, active signals
- **Live Signals** - Generate sinyal BELI/JUAL dengan Entry, SL, TP
- **Market Chart** - TradingView candlestick chart real-time
- **Signal Tracking** - Track otomatis SL/TP dengan auto-update status

### Research Lab
- **Backtest Engine** - Test strategi dengan data historis CSV
- **Data Manager** - Upload, kelola, dan proses data CSV
- **ML Training** - Train LSTM model untuk prediksi lebih akurat

### Multi-Market Support
- **Binance Spot** - Trading spot dengan harga real-time
- **Binance Futures** - Trading futures dengan leverage, funding rate, open interest

### Dynamic Symbol Selection
- Cari coin apapun yang ada di Binance
- Tambahkan ke favorites dengan label SPOT/FUTURES
- Watchlist dengan harga real-time

### Hybrid Signal Generator
- **Technical Analysis**: RSI, EMA, ATR, Support/Resistance, Divergence
- **AI Prediction**: LSTM Deep Learning untuk prediksi arah harga
- **Confluence System**: Kombinasi Technical + AI untuk sinyal lebih akurat

### Signal Tracking
- Catat semua sinyal yang di-generate
- Track otomatis SL/TP
- Statistik win rate dan PnL
- Auto-tracking service

### Real-time Data
- WebSocket connection ke Binance
- Harga update real-time dengan flash animation
- 24h change indicator

## Tech Stack

- **Backend**: FastAPI + SQLAlchemy + SQLite
- **Frontend**: HTML5 + CSS3 + JavaScript (Vanilla)
- **AI**: TensorFlow/LSTM (simulasi jika TF tidak tersedia)
- **Data**: Binance API (Spot & Futures)

## Struktur Project

```
├── backend/
│   ├── api/           # Route handlers
│   ├── core/          # Config & constants
│   ├── models/        # Database models
│   ├── services/      # Business logic
│   └── utils/         # Helper functions
├── frontend/
│   ├── css/           # Stylesheets
│   ├── js/            # JavaScript modules
│   └── index.html     # Main HTML
├── data/
│   ├── database/      # SQLite database
│   ├── models/        # Trained ML models
│   ├── processed/     # Processed CSV data
│   └── uploads/       # Raw CSV uploads
└── docs/
    └── DOCS.md        # Documentation
```

## Cara Menjalankan

```bash
# Install dependencies
pip install -r requirements.txt

# Jalankan server
python -m uvicorn backend.app:app --reload --port 8000

# Buka browser
http://localhost:8000
```

## API Endpoints

### Binance
- `GET /binance/spot/prices` - Harga spot
- `GET /binance/futures/prices` - Harga futures
- `GET /binance/search?query=BTC` - Cari symbol
- `GET /binance/futures/funding/{symbol}` - Funding rate

### Signals
- `POST /signals/create` - Buat sinyal baru
- `GET /signals/active` - Sinyal yang masih open
- `GET /signals/history` - History sinyal
- `GET /signals/statistics` - Statistik performa

### Favorites
- `POST /signals/favorites/add` - Tambah favorit
- `GET /signals/favorites` - List favorit
- `DELETE /signals/favorites/{symbol}` - Hapus favorit

### Analysis
- `POST /hybrid/analyze/{symbol}` - Hybrid analysis (Technical + AI)
- `GET /lstm/predict/{symbol}` - AI prediction only

## Trading Modes

| Mode | Holding | RSI Period | Risk:Reward |
|------|---------|------------|-------------|
| Aktif | 1-4 jam | 6 | 1:2 |
| Santai | 4-12 jam | 8 | 1:2.5 |
| Pasif | 12-24 jam | 14 | 1:3 |

## License

MIT License - Leon Liquidity Engine
