# Feature Dictionary — NYC Taxi Demand 2026

Dataset hasil `script/05_features.ipynb`. Sumber: `datasets/interim/2026/main_trips.parquet`.

- Unit analisis: **satu zona pickup × satu jam**.
- Target regresi: `target_pickup_count` = jumlah pickup pada jam T.
- Target klasifikasi: `demand_level` = Rendah / Sedang / Tinggi.
- Fitur historis dihitung dari jam **sebelum T** (sudah di-shift), jadi tidak bocor.

## 1. Kolom Dataset (`features_dataset.parquet`)

| Kolom | Tipe | Definisi | Tujuan | Tersedia saat prediksi? |
|:--|:--|:--|:--|:--:|
| `hour` | datetime | Timestamp jam (key, bukan fitur) | pengenal waktu | – |
| `zone_id` | int | ID zona (LocationID) | key zona | – |
| `PU_longitude` | float | Longitude centroid zona pickup | fitur lokasi | Ya |
| `PU_latitude` | float | Latitude centroid zona pickup | fitur lokasi | Ya |
| `PU_zone_name` | str | Nama zona pickup | label | Ya |
| `PU_borough` | str | Borough zona pickup | fitur kategori | Ya |
| `is_airport` | 0/1 | Zona bandara (EWR, JFK, LGA, Newark) | fitur zona | Ya |
| `is_cbd` | 0/1 | Zona CBD (borough Manhattan) | fitur zona | Ya |
| `hour_of_day` | int | Jam 0–23 dari `hour` | fitur waktu | Ya |
| `day_of_week` | int | Hari 0–6 (0 = Senin) | fitur waktu | Ya |
| `month` | int | Bulan 1–12 | fitur waktu | Ya |
| `is_weekend` | 0/1 | 1 kalau Sabtu/Minggu | fitur waktu | Ya |
| `is_holiday` | 0/1 | 1 kalau tanggal libur/event (brief 3.7) | fitur waktu | Ya |
| `lag_1` | float | Pickup pada T-1 | fitur historis | Ya |
| `lag_24` | float | Pickup pada T-24 jam | fitur historis | Ya |
| `lag_168` | float | Pickup pada T-168 jam (minggu lalu) | fitur historis | Ya |
| `roll_24` | float | Rata-rata pickup T-24..T-1 | ringkasan historis | Ya |
| `roll_168` | float | Rata-rata pickup T-168..T-1 | ringkasan historis | Ya |
| `target_pickup_count` | int | Jumlah pickup pada jam T | **target regresi** | Tidak (target) |
| `demand_level` | kategori | Rendah / Sedang / Tinggi dari `target_pickup_count` | **target klasifikasi** | Tidak (target) |
| `split` | str | train / validation / test | metadata | Tidak |

## 2. Kolom Dataset Grid (`demand_zone_hour.parquet`)

Grid zona-jam lengkap (263 zona × 4.344 jam).

| Kolom | Tipe | Keterangan |
|:--|:--|:--|
| `hour` | datetime | jam |
| `zone_id` | int | ID zona |
| `PU_longitude`, `PU_latitude` | float | centroid zona |
| `PU_zone_name`, `PU_borough` | str | atribut zona |
| `is_airport`, `is_cbd` | 0/1 | atribut zona |
| `pickup_count` | int/NaN | jumlah pickup jam itu (0 kalau tidak ada; NaN di jam DST) |
| `is_dst_missing` | 0/1 | 1 di 2026-03-08 02:00 (jam tidak ada karena DST) |

## 3. Aturan Anti-Leakage

Fitur yang **tidak boleh** dipakai:

- Koordinat dropoff (`DO_longitude`, `DO_latitude`): tujuan belum diketahui saat menunggu penumpang.
- Nilai transaksi pasca-perjalanan: `fare_amount`, `total_amount`, `tip_amount`, `cbd_congestion_fee`, `trip_distance`, `passenger_count`.
- Lag/rolling yang tidak di-shift.
- Scaler dan batas kelas yang dihitung dari validation/test.

Pemeriksaan di notebook:
- `target_pickup_count` tidak masuk daftar fitur.
- `lag_1` dicek sama dengan pickup jam sebelumnya.
- Kolom terlarang tidak ada di daftar fitur.

## 4. Definisi `demand_level`

- Batas kelas dari **data training saja** (Januari–April), pakai tercile 33/66.
- Nilai batas yang didapat: **Rendah <= 0**, **Sedang <= 4**, **Tinggi > 4**.
- Distribusi kelas di training: Rendah 37,9%, Sedang 31,0%, Tinggi 31,1%.

## 5. Split Kronologis

| Bagian | Periode | Baris |
|:--|:--|--:|
| train | 2026-01-08 s/d 2026-04-30 | 668.809 |
| validation | 2026-05-01 s/d 2026-05-31 | 195.672 |
| test | 2026-06-01 s/d 2026-06-30 | 189.360 |
| **Total** | | **1.053.841** |

Awal train 8 Januari karena `lag_168` butuh 168 jam riwayat per zona.

## 6. Catatan

- Jam DST 2026-03-08 02:00 ditandai **tidak tersedia** (`is_dst_missing=1`, `pickup_count=NaN`), bukan nol, dan barisnya tidak dipakai di modeling.
- `is_holiday` dibangun dari tabel brief 3.7. Kalau Anggota 4 menyediakan file kalender di `datasets/external/`, kolom ini bisa diganti.
- `PU_borough` masih berupa teks; perlu di-encode (one-hot / ordinal) di tahap modeling.
