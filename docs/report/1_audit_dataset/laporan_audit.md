# Laporan Audit Dataset — NYC Yellow Taxi 2026

Ringkasan hasil audit 6 file Parquet Januari–Juni 2026 sebelum masuk proses cleaning.
Detail tabel mentah ada di `rentang_tiap_dataset.md` dan `missing_value.md`.

## 1. Kelengkapan File

Semua 6 file ada, bisa dibaca, dan tidak corrupt.

| Bulan | Nama file | Ukuran | Baris | Kolom |
|:--|:--|--:|--:|--:|
| Jan | yellow_tripdata_2026-01.parquet | 61,19 MB | 3.724.889 | 20 |
| Feb | yellow_tripdata_2026-02.parquet | 55,96 MB | 3.399.866 | 20 |
| Mar | yellow_tripdata_2026-03.parquet | 64,75 MB | 3.952.451 | 20 |
| Apr | yellow_tripdata_2026-04.parquet | 61,82 MB | 3.831.240 | 20 |
| Mei | yellow_tripdata_2026-05.parquet | 66,47 MB | 4.090.836 | 20 |
| Jun | yellow_tripdata_2026-06.parquet | 62,43 MB | 3.837.248 | 21 |
| **Total** | | | **22.836.530** | |

## 2. Skema Kolom

- Bulan Januari–Mei punya **20 kolom** dengan nama dan tipe data yang sama.
- Bulan Juni punya **21 kolom**: ada tambahan `request_source`.
- `request_source` hanya ada di Juni dan **73,60%** isinya kosong, jadi diputuskan **dibuang** biar skema 6 bulan seragam.
- Tidak ada kolom yang kosong seluruhnya.

## 3. Missing Value

Lima kolom ini kosong dengan jumlah yang sama tiap bulan (kemungkinan baris yang sama kosong di kelimanya):

| Bulan | passenger_count | RatecodeID | store_and_fwd_flag | congestion_surcharge | Airport_fee |
|:--|--:|--:|--:|--:|--:|
| Jan | 1.088.058 (29,21%) | 1.088.058 | 1.088.058 | 1.088.058 | 1.088.058 |
| Feb | 1.023.317 (30,10%) | 1.023.317 | 1.023.317 | 1.023.317 | 1.023.317 |
| Mar | 945.748 (23,93%) | 945.748 | 945.748 | 945.748 | 945.748 |
| Apr | 799.786 (20,88%) | 799.786 | 799.786 | 799.786 | 799.786 |
| Mei | 955.371 (23,35%) | 955.371 | 955.371 | 955.371 | 955.371 |
| Jun | 1.013.500 (26,41%) | 1.013.500 | 1.013.500 | 1.013.500 | 1.013.500 |

Kolom kunci (`tpep_pickup_datetime`, `tpep_dropoff_datetime`, `PULocationID`, `DOLocationID`, `fare_amount`, `total_amount`) **tidak ada yang kosong**.

Karena kelima kolom yang kosong itu cuma kolom pendukung (bukan wajib untuk analisis demand), **tidak ada baris yang dibuang hanya karena missing value**. Nilai kosong dibiarkan dan baru ditangani di tahap model bila perlu.

## 4. Anomali yang Ketemu

- Ada baris dengan pickup **di luar Januari–Juni 2026** (mis. tahun 2001, 2008, 2025-12-31, atau bulan berikutnya). Jumlahnya kecil dan dibuang di cleaning (aturan C1).
- Ada `fare_amount` **negatif** (mis. -70) dan tarif ekstrem. Ditangani di cleaning (C8).
- Ada durasi tidak wajar (dropoff sebelum pickup / sangat panjang). Ditangani di cleaning (C3).
- Ada `PULocationID` / `DOLocationID` bernilai zona Unknown (264/265). Dibuang di cleaning (C4/C5).

## 5. Kesimpulan

Dataset **layak dipakai** untuk analisis dan modeling:

- Cakupan 6 bulan cukup untuk split kronologis: Train Jan–Apr, Validation Mei, Test Juni.
- Volume ~22,8 juta baris cukup untuk EDA, analisis spasial, dan modeling.
- Kolom waktu dan lokasi pickup lengkap, jadi target `pickup_count` per zona per jam bisa dibentuk.
- Data 2016 tetap dipisah dan tidak digabung ke deret 2026.

Syarat lanjut: lewati cleaning dulu (lihat `docs/report/2a_cleaning/laporan_cleaning.md`).
