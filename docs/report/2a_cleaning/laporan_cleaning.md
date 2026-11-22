# Laporan Data Cleaning (Fase 2A & 2B)

Hasil cleaning 6 file Yellow Taxi 2026 (Januari–Juni). Sumber aturan: `docs/analysis_plan.md` bagian 4.
Dijalankan dari `script/1_data_cleaning.ipynb`.

## 1. Ringkasan

| Item | Nilai |
|:--|--:|
| Baris awal | 22.836.530 |
| Baris dibuang | 561.980 |
| Baris akhir (`main_trips`) | 22.274.550 |
| Persentase dibuang | 2,46% |

Sebagian besar data lolos. Pembuangan terbesar dari durasi tidak wajar (C3) dan tarif tidak wajar (C8).

## 2. Hasil per Aturan

| Aturan | Baris sebelum | Baris dibuang | Baris sesudah | % dibuang |
|:--|--:|--:|--:|--:|
| C1 - Pickup di luar Jan-Jun 2026 | 22.836.530 | 15 | 22.836.515 | 0,0001 |
| C2 - Timestamp kosong | 22.836.515 | 0 | 22.836.515 | 0,0000 |
| C3 - Durasi tidak wajar | 22.836.515 | 286.366 | 22.550.149 | 1,2540 |
| C4 - Zona pickup tidak valid | 22.550.149 | 35.923 | 22.514.226 | 0,1593 |
| C5 - Zona dropoff tidak valid | 22.514.226 | 108.256 | 22.405.970 | 0,4808 |
| C6 - Duplikat seluruh baris | 22.405.970 | 0 | 22.405.970 | 0,0000 |
| C7 - `trip_distance` tidak wajar | 22.405.970 | 616 | 22.405.354 | 0,0027 |
| C8 - Tarif tidak wajar | 22.405.354 | 130.786 | 22.274.568 | 0,5837 |
| C9 - Jumlah penumpang tidak wajar | 22.274.568 | 18 | 22.274.550 | 0,0001 |
| C10 - Kode kategori tidak dikenal | 22.274.550 | 0 | 22.274.550 | 0,0000 |
| **Total** | **22.836.530** | **561.980** | **22.274.550** | **2,4609** |

Catatan tiap aturan:
- **C3** membuang `286.366` baris (durasi <= 0 menit atau > 24 jam), kontributor terbesar.
- **C8** membuang `130.786` baris (tarif/jarak negatif atau > $500).
- **C5** membuang `108.256` baris (zona dropoff Unknown/264/265/di luar 1-263).
- **C6**, **C10** nol: tidak ada duplikat penuh dan tidak ada kode kategori asing.
- Nilai kosong pada kolom pendukung (`passenger_count`, `RatecodeID`, dll.) **dibiarkan**, bukan dihapus, sesuai aturan di `analysis_plan.md`.

## 3. Pembersihan Skema

- Kolom `request_source` (hanya ada di Juni, 73,6% kosong) dibuang supaya 20 kolom seragam di semua bulan.
- Tipe data disamakan antarbulan sebelum digabung.

## 4. Ganti ID Lokasi jadi Koordinat (Fase 2B)

- Sumber: `datasets/zone/taxi_zone.parquet` yang sudah berisi `latitude`/`longitude` (centroid WGS84) per zona. Tidak perlu hitung ulang.
- Hasil pemetaan: `datasets/zone/zone_centroid_lookup.csv` berisi `LocationID, longitude, latitude, zone_name, borough, is_airport, is_cbd`.
- Jumlah zona: **263** (ID 1-263). Zona 264 (Unknown) dan 265 (Outside of NYC) sudah dibuang di C4/C5.
- Zona tanpa koordinat: **0**.
- Join `PULocationID` → `PU_longitude/PU_latitude` dan `DOLocationID` → `DO_longitude/DO_latitude` (left join, tidak menambah baris).
- Kolom `PULocationID` dan `DOLocationID` dilepas dari `main_trips`. File di `datasets/raw/` tetap utuh.

Atribut zona:
- `is_airport = 1` untuk borough EWR atau zona yang namanya mengandung airport/newark/jfk/laguardia.
- `is_cbd = 1` untuk borough Manhattan.

## 5. Output

| File | Isi |
|:--|:--|
| `datasets/interim/2026/main_trips.parquet` | 22.274.550 baris × 31 kolom, 544,2 MB |
| `datasets/zone/zone_centroid_lookup.csv` | 263 zona + centroid + atribut |
| `out/output_eda/03_cleaning_log.csv` | tabel attrition (tabel di atas) |

Kolom `main_trips`: waktu (2), koordinat & atribut pickup (6), koordinat & atribut dropoff (6), atribut perjalanan & biaya (16), `_bulan` (1).

## 5.1 Konsentrasi Penghapusan

Dicek per tanggal (`04_cleaning_concentration.csv`). Penghapusan **tidak terkonsentrasi** di tanggal/periode tertentu:

- C3–C8: porsi terbesar pada satu tanggal < 2% (mis. C3 maks 0,75% di 2026-05-14, C8 maks 1,13% di 2026-01-03).
- C1: 40% ada di 2025-12-31, tapi totalnya cuma 15 baris.
- C9: 5,56% di 2026-01-03, tapi totalnya cuma 18 baris.

## 6. Kesimpulan

- Cleaning selesai, sisa **22.274.550** baris (97,54% data awal).
- Semua baris di `main_trips` sudah punya lokasi pickup valid dalam rentang Januari–Juni 2026, jadi siap dipakai untuk agregasi `demand_zone_hour` dan modeling.
- Data sudah memakai koordinat centroid zona, bukan ID lokasi.
