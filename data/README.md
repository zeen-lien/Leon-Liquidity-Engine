## Folder `data/`

Folder ini digunakan untuk menyimpan file **data historis** dalam format CSV,
misalnya data candlestick 1 menit (1m) dari Binance.

### Cara pakai singkat

1. Simpan file data historis OHLCV 1 menit kamu ke dalam folder ini.
2. Untuk contoh backtest di `contoh_backtest_dari_csv.py`, gunakan nama file:

- `data/historis_1.csv`

Pastikan file memiliki kolom minimal (format standar kline Binance 1m):
- `open_time`
- `open`
- `high`
- `low`
- `close`
- `volume`


