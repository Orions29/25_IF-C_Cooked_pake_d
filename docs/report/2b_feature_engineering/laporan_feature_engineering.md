# Laporan Feature Engineering (Fase 5)

Mengubah `main_trips` jadi dataset siap model. Dijalankan dari `script/05_features.ipynb`.
Kamus fitur lengkap: `docs/feature_dictionary.md`.

## 1. Alur

1. Agregasi pickup per **zona × jam** dari `main_trips`.
2. Bentuk **grid zona-jam lengkap** (263 zona × 4.344 jam). Zona-jam tanpa pickup = 0.
3. Tambah fitur waktu, libur, lokasi, lag, dan rolling mean.
4. Tentukan target regresi + target klasifikasi.
5. Split kronologis dan cek leakage.
6. Simpan dataset + deret waktu.

## 2. Angka Kunci

| Item | Nilai |
|:--|--:|
| Grid zona-jam (`demand_zone_hour`) | 1.142.472 baris |
| Zona | 263 |
| Jam (Jan–Jun 2026) | 4.344 |
| Zona-jam berisi pickup | 685.384 (60,0%) |
| Zona-jam bernilai nol | 40,0% |
| Dataset fitur (`features_dataset`) | 1.053.841 baris, 15 fitur |

Total pickup di grid = total pickup di `main_trips` = **22.274.550** (cocok).

## 3. Fitur

- **Waktu:** `hour_of_day`, `day_of_week`, `month`, `is_weekend`, `is_holiday`, `is_major_nyc_event`
- **Lokasi:** `PU_longitude`, `PU_latitude`, `is_airport`, `is_cbd`, `PU_borough`
- **Historis (di-shift):** `lag_1`, `lag_24`, `lag_168`
- **Rolling (di-shift):** `roll_24`, `roll_168`

## 4. Target

- Regresi: `target_pickup_count` (jumlah pickup jam T).
- Klasifikasi: `demand_level` (Rendah/Sedang/Tinggi).
  - Batas dari data training saja (tercile 33/66): **Rendah <= 0, Sedang <= 4, Tinggi > 4**.
  - Distribusi train: Rendah 37,9%, Sedang 31,0%, Tinggi 31,1%.

## 5. Split Kronologis

| Bagian | Periode | Baris |
|:--|:--|--:|
| train | 8 Jan – 30 Apr 2026 | 668.809 |
| validation | 1 – 31 Mei 2026 | 195.672 |
| test | 1 – 30 Jun 2026 | 189.360 |

Train mulai 8 Januari karena `lag_168` butuh 168 jam riwayat per zona.

## 6. Pemeriksaan Leakage

- `target_pickup_count` tidak masuk daftar fitur.
- `lag_1` sudah dicek = pickup jam sebelumnya.
- Tidak ada koordinat dropoff dan nilai transaksi di fitur.
- `pickup_count` mentah tidak ikut disimpan di `features_dataset` (cuma ada di grid), biar tidak kepakai sebagai fitur.

## 7. Deret Waktu (untuk Anggota 3)

- **Kota keseluruhan:** `timeseries_city.parquet` (4.344 jam).
- **Top-5 zona:** `timeseries_top5.parquet` (21.720 baris).

Top-5 zona berdasarkan total pickup:

1. Upper East Side South (zone 237) — 941.964
2. Upper East Side North (zone 236) — 853.602
3. Midtown Center (zone 161) — 844.602
4. JFK Airport (zone 132) — 740.047
5. Midtown East (zone 162) — 622.635

## 8. Output

| File | Isi |
|:--|:--|
| `datasets/interim/2026/demand_zone_hour.parquet` | grid zona-jam (1.142.472 × 10) |
| `datasets/interim/2026/features_dataset.parquet` | dataset fitur + target + split (1.053.841 × 22) |
| `datasets/interim/2026/timeseries_city.parquet` | deret pickup kota per jam |
| `datasets/interim/2026/timeseries_top5.parquet` | deret pickup Top-5 zona |
| `docs/feature_dictionary.md` | kamus fitur |

## 9. Catatan

- Jam DST 8 Maret 2026 02:00 ditandai tidak tersedia, bukan nol.
- `is_holiday` (libur federal) dan `is_major_nyc_event` diambil dari `datasets/processed/nyc_holiday_event_calendar_2026.csv` (kalender resmi Anggota 4).
- `PU_borough` masih teks, perlu di-encode saat modeling.
