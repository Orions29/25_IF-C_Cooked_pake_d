# Analysis Plan — NYC Yellow Taxi Demand Analytics 2026

> **Lokasi file:** `docs/analysis_plan.md`
> **Cara pakai:** isi bagian bertanda `____` atau `TBD`. Bagian yang sudah terisi berasal dari brief dan hanya boleh diubah dengan alasan tertulis di **Bagian 14 (Log Perubahan Keputusan)**.
> **Status keputusan:** `Draft` = belum final · `Final` = sudah diperiksa terhadap data dan disetujui tim.
> **Prinsip:** jangan menganggap aturan atau ambang cleaning sudah final sebelum memeriksa distribusi data dan menuliskan alasannya. Jangan mengubah aturan hanya karena hasil awal tidak sesuai harapan.

|                                  |                                                |
| :------------------------------- | :--------------------------------------------- |
| **Versi dokumen**                | v0.1                                           |
| **Terakhir diperbarui**          | 1 November 2026                                |
| **Penanggung jawab**             | Rio Meidi A                                    |
| **Anggota tim**                  | Rio Meidi A, Anggota 2 , Aushaf Fathin I N , Anggota 4 |
| **Seed global (`random_state`)** | 42                                             |

---

## 1. Tujuan & Pertanyaan Penelitian

**Tujuan:** memahami pola pickup taksi kuning, menemukan hotspot, dan memodelkan permintaan per zona per jam.

| Kode | Pertanyaan                                                                                           | Dijawab di    | Penanggung jawab | Status jawaban |
| :--: | :--------------------------------------------------------------------------------------------------- | :------------ | :--------------- | :------------- |
| RQ1  | Bagaimana pola pickup berdasarkan jam, hari, dan bulan?                                              | Fase 3        | Mufid (Anggota 2)  | [ ]            |
| RQ2  | Zona mana yang menjadi hotspot / cold spot, dan apakah stabil antarbulan?                            | Fase 4B       | Aushaf (Anggota 3) | [ ]            |
| RQ3  | Seberapa akurat model memprediksi pickup per zona per jam, dan model mana yang paling layak dipilih? | Fase 6, 7     | Erlan (Anggota 4)  | [ ]            |
| RQ4  | Zona dan waktu mana yang layak diprioritaskan berdasarkan volume pickup?                             | Fase 3, 4B, 7 | Mufid & Erlan      | [ ]            |

**Catatan interpretasi:** jumlah pickup adalah _served demand_ (perjalanan yang berhasil dilayani), bukan seluruh permintaan taksi yang sebenarnya.

**Batas ruang lingkup:** pekerjaan berakhir di Fase 7 (Optimasi & Trade-off). Laporan akhir dan rekomendasi operasional di luar dokumen ini.

---

## 2. Dataset & Periode

| Item          | Keputusan                                | Status |
| :------------ | :--------------------------------------- | :----: |
| Sumber        | NYC TLC, Yellow Taxi Trip Records        | Final  |
| Dataset utama | **2026**                                 | Final  |
| Periode       | **Januari - Juni 2026** (6 file Parquet) | Final  |
| Zona waktu    | Waktu lokal New York                     | Final  |

### 2.1 Inventaris File _(diisi setelah Fase 1)_

| Bulan     | Nama file                       |   Ukuran | Jumlah baris | Jumlah kolom | Rentang pickup (min - maks)               | Catatan |
| :-------- | :------------------------------ | -------: | -----------: | -----------: | :---------------------------------------- | :------ |
| Jan       | yellow_tripdata_2026-01.parquet | 61.19 MB |      3724889 |           20 | 2026-01-01 00:54:04 - 2026-01-31 23:43:12 |         |
| Feb       | yellow_tripdata_2026-02.parquet | 55.96 MB |      3399866 |           20 | 2026-02-01 00:05:57 - 2026-02-28 23:13:53 |         |
| Mar       | yellow_tripdata_2026-03.parquet | 64.75 MB |      3952451 |           20 | 2026-03-01 00:02:26 - 2026-03-31 23:14:21 |         |
| Apr       | yellow_tripdata_2026-04.parquet | 61.82 MB |      3831240 |           20 | 2026-04-01 00:40:05 - 2026-04-30 23:58:15 |         |
| Mei       | yellow_tripdata_2026-05.parquet | 66.47 MB |      4090836 |           20 | 2026-05-01 00:04:59 - 2026-05-31 23:41:51 |         |
| Jun       | yellow_tripdata_2026-06.parquet | 62.43 MB |      3837248 |           21 | 2026-06-01 00:04:22 - 2026-06-30 23:50:27 |         |
| **Total** | 6 file Parquet                  | 372.62 MB |       22836530 |              |                                           |         |

#### Catatan

- di Tabel bulan juni ada tambahan kolom request_source yang harusnya dari 20 jadi 21. Direncanakan akan dihapus

### 2.2 Temuan Skema _(diisi setelah Fase 1)_

- Konsistensi nama kolom dan tipe data antarbulan: Semua sesuai tipedatanya kecuali ada kelebihan kolom pada bulan 6
- Kolom yang kosong seluruhnya / hanya ada pada bulan tertentu: tidak ada
- Status kolom `request_source` (ada / tidak): ada tapi mau dihapus aja
- Apakah dataset 2026 sesuai tujuan penelitian: Ya sepertinya

---

## 3. Representasi Lokasi

| Item                                   | Keputusan                                                                                                                        | Status |
| :------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------- | :----: |
| Representasi lokasi                    | Longitude & latitude **centroid zona** (bukan GPS asli)                                                                          | Final  |
| `PULocationID`                         | Diganti `PU_longitude`, `PU_latitude` di `main_trips`                                                                            | Final  |
| `DOLocationID`                         | Diganti `DO_longitude`, `DO_latitude` di `main_trips`                                                                            | Final  |
| ID asli                                | Tetap ada di `datasets/raw/`; ID hanya dilepas pada salinan di `interim/`                                                        | Final  |
| Sumber geometri                        | Taxi Zone Lookup / Shapefile TLC di `datasets/zone/`                                                                             | Final  |
| CRS centroid                           | WGS84 (EPSG:4326)                                                                                                                | Final  |
| Tabel pemetaan                         | `datasets/zone/zone_centroid_lookup.csv` (`LocationID`, `longitude`, `latitude`, `zone_name`, `borough`, `is_airport`, `is_cbd`) | Final  |
| Jenis join                             | _Left join_; jumlah baris tidak boleh bertambah                                                                                  | Final  |
| Atribut zona turunan                   | `borough`, `zone_name`, `is_airport`, `is_cbd` (diturunkan **sebelum** ID dilepas)                                               | Final  |
| Perlakuan zona _Unknown_ (ID 264, 265) | ☑ Dibuang · ☐ Dilabeli khusus — alasan: zona tidak punya geometri/koordinat, tidak bisa direpresentasikan sebagai titik pickup | Final  |
| Definisi `is_airport`                  | Borough = 'EWR' atau nama zona mengandung 'airport' / 'newark' / 'jfk' / 'laguardia'                                             | Final  |
| Definisi `is_cbd`                      | Borough = 'Manhattan'                                                                                                            | Final  |

**Hasil pemeriksaan tabel centroid** _(diisi setelah Fase 2B)_

- [x] Satu zona = satu record
- [x] Pasangan koordinat unik per zona
- [x] Semua koordinat berada di wilayah NYC
- [x] Zona tanpa geometri tercatat: 264 (Unknown) dan 265 (Outside of NYC) — dibuang di C4/C5
- [x] Jumlah baris `main_trips` sebelum dan sesudah join sama: **22.274.550 / 22.274.550**

---

## 4. Aturan Cleaning

> Tulis aturan **sebelum** diterapkan. Tentukan batas dari distribusi data dan dokumentasi TLC, bukan dari tebakan. Aturan outlier tidak boleh membuang perjalanan yang sebenarnya valid.

### 4.1 Dua Jalur Validitas

| Jalur                    | Syarat valid                                                   | Dipakai untuk                                  |
| :----------------------- | :------------------------------------------------------------- | :--------------------------------------------- |
| **Demand**               | Waktu pickup valid, lokasi pickup valid, dalam rentang periode | `main_trips` → `demand_zone_hour`, semua model |
| **Revenue** _(opsional)_ | Syarat demand + nilai transaksi layak (tarif, jarak, durasi)   | `revenue_analysis`                             |

Baris dengan tarif/jarak bermasalah **tidak otomatis dibuang** dari jalur demand.

### 4.2 Daftar Aturan

| ID  | Aturan                                           | Kolom                                           | Batas / kriteria                                      | Jalur                       | Alasan & bukti distribusi                                                                                          | Status |
| :-- | :----------------------------------------------- | :---------------------------------------------- | :---------------------------------------------------- | :-------------------------- | :----------------------------------------------------------------------------------------------------------------- | :----: |
| C1  | Pickup di luar rentang Jan-Jun 2026              | `tpep_pickup_datetime`                          | < 2026-01-01 atau > 2026-06-30 23:59:59               | Demand + Revenue            | Audit menemukan pickup tahun 2001/2008 dan bulan di luar Jan-Jun 2026                                              | Final  |
| C2  | Timestamp kosong / tidak valid                   | `tpep_pickup_datetime`, `tpep_dropoff_datetime` | salah satu kolom kosong                               | Demand + Revenue            | Kolom waktu wajib untuk demand dan agregasi zona-jam                                                               | Final  |
| C3  | Dropoff sebelum pickup / durasi tidak wajar      | durasi = dropoff − pickup                       | <= 0 menit atau > 1440 menit (24 jam)                 | Demand + Revenue            | Tidak masuk akal secara fisik; tidak ada yang signifikan                                                         | Final  |
| C4  | Zona pickup kosong / di luar daftar / _Unknown_  | `PULocationID`                                  | kosong / di luar 1–263 / Unknown (264, 265)           | Demand + Revenue            | Lokasi pickup wajib untuk analisis demand dan join koordinat                                                     | Final  |
| C5  | Zona dropoff kosong / di luar daftar / _Unknown_ | `DOLocationID`                                  | kosong / di luar 1–263 / Unknown (264, 265)           | Demand + Revenue            | Koordinat dropoff perlu valid di `main_trips` tunggal                                                              | Final  |
| C6  | Duplikat seluruh baris                           | seluruh kolom                                   | baris identik                                         | Demand + Revenue            | Menghindari perhitungan ganda perjalanan yang sama                                                                 | Final  |
| C7  | `trip_distance` nol / negatif / ekstrem          | `trip_distance`                                 | negatif / > 100 mil (nilai kosong dibiarkan)          | Demand + Revenue            | Jarak > 100 mil atau negatif tidak wajar untuk taksi NYC                                                           | Final  |
| C8  | `fare_amount`, `total_amount` negatif / ekstrem  | `fare_amount`, `total_amount`                   | negatif / > $500 (nilai kosong dibiarkan)             | Demand + Revenue            | Audit menemukan tarif negatif (mis. fare_amount = -70)                                                             | Final  |
| C9  | `passenger_count` nol / ekstrem                  | `passenger_count`                               | negatif / > 6 (nilai kosong dibiarkan)                | Demand + Revenue            | Jumlah penumpang taksi wajar max 6; ~20–30% missing per bulan dibiarkan, bukan dibuang                            | Final  |
| C10 | Kode kategori tidak dikenal                      | `VendorID`, `RatecodeID`, `payment_type`        | di luar daftar referensi TLC (nilai kosong dibiarkan) | Demand + Revenue            | VendorID∈{1,2,6,7}, RatecodeID∈{1,2,3,4,5,6,99}, payment_type∈{0,1,2,3,4,5,6}; NaN RatecodeID dibiarkan           | Final  |
| C11 | \_\_\_\_                                         | \_\_\_\_                                        | \_\_\_\_                                              | \_\_\_\_                    |                                                                                                                    | Draft  |

### 4.3 Penanganan Missing Values

| Kolom | % kosong | Fungsi kolom | Strategi (buang baris / isi / biarkan / buang kolom) | Alasan |
| :---- | -------: | :----------- | :--------------------------------------------------- | :----- |
| `passenger_count` | ~20–30 | atribut penumpang (revenue) | Biarkan di `main_trips` (tidak dibuang hanya karena ini) | Kolom pendukung, tidak wajib untuk jalur demand |
| `RatecodeID` | ~20–30 | kode tarif (revenue) | Biarkan | Kolom pendukung revenue |
| `store_and_fwd_flag` | ~20–30 | flag penyimpanan | Biarkan | Tidak mempengaruhi demand |
| `congestion_surcharge` | ~20–30 | biaya kemacetan (revenue) | Biarkan | Kolom pendukung revenue |
| `Airport_fee` | ~20–30 | biaya bandara (revenue) | Biarkan | Kolom pendukung revenue |
| `request_source` (hanya Bulan 6) | 73,6% | sumber permintaan | Buang kolom pada Bulan 6 | Hanya ada di Bulan 6, sebagian besar kosong |

Tidak ada baris yang dihapus hanya karena satu kolom pendukung kosong. Baris dihapus hanya jika melanggar aturan C1-C10 (nilai kosong pada kolom pendukung tidak dihitung pelanggaran).

### 4.4 Duplikat

- Definisi duplikat: seluruh baris identik di semua kolom.
- Hasil pemeriksaan: dihapus via `drop_duplicates()` (catatan berulang diperlakukan sebagai duplikat, bukan perjalanan berbeda, karena semua atribut termasuk waktu lokasi identik).
- Aturan penghapusan: satu baris tetap, duplikat buang; dicatat di `03_cleaning_log.csv` (C6).

### 4.5 Kolom Wajib untuk Analisis

| Jalur   | Kolom wajib |
| :------ | :---------- |
| Demand  | `tpep_pickup_datetime`, `PULocationID` (lalu diganti `PU_longitude`/`PU_latitude`) |
| Revenue | `tpep_pickup_datetime`, `PULocationID`, `DOLocationID`, `trip_distance`, `fare_amount`, `total_amount`, `passenger_count` |

### 4.6 Log Cleaning (_attrition_)

Diisi otomatis dari notebook `1_data_cleaning.ipynb`. Berkas: `out/output_eda/03_cleaning_log.csv`.

| Aturan    | Baris sebelum | Baris dibuang | Baris sesudah | % dibuang | Konsentrasi pada tanggal/periode tertentu? |
| :-------- | ------------: | ------------: | ------------: | --------: | :----------------------------------------- |
| C1        |    22.836.530 |            15 |    22.836.515 |    0,0001 | Tidak (maks 40% di 2025-12-31, tapi cuma 15 baris) |
| C2        |    22.836.515 |             0 |    22.836.515 |    0,0000 | – |
| C3        |    22.836.515 |       286.366 |    22.550.149 |    1,2540 | Tidak (maks 0,75% di 2026-05-14) |
| C4        |    22.550.149 |        35.923 |    22.514.226 |    0,1593 | Tidak (maks 0,90% di 2026-06-13) |
| C5        |    22.514.226 |       108.256 |    22.405.970 |    0,4808 | Tidak (maks 0,88% di 2026-06-14) |
| C6        |    22.405.970 |             0 |    22.405.970 |    0,0000 | – (tidak ada duplikat penuh) |
| C7        |    22.405.970 |           616 |    22.405.354 |    0,0027 | Tidak (maks 1,46% di 2026-02-26) |
| C8        |    22.405.354 |       130.786 |    22.274.568 |    0,5837 | Tidak (maks 1,13% di 2026-01-03) |
| C9        |    22.274.568 |            18 |    22.274.550 |    0,0001 | Tidak (maks 5,56% di 2026-01-03, cuma 18 baris) |
| C10       |    22.274.550 |             0 |    22.274.550 |    0,0000 | – (tidak ada kode asing) |
| **Total** | **22.836.530** |   **561.980** | **22.274.550** | **2,4609** | Tidak terkonsentrasi di satu tanggal |

### 4.7 Anomali & Penanganannya

| Anomali | Cara menemukan | Kesalahan pencatatan atau kejadian nyata? | Keputusan |
| :------ | :------------- | :---------------------------------------- | :-------- |
| Tarif negatif (`fare_amount` < 0) | Hitung `fare_amount < 0` per bulan (`02_data_quality.csv`) | Kesalahan pencatatan | Dibuang (C8) |
| Durasi <= 0 atau > 24 jam | `durasi = dropoff - pickup` | Kesalahan argometer / pencatatan | Dibuang (C3) |
| Pickup di luar Jan–Jun 2026 | Bandingkan dengan rentang periode | Data nyasar / salah input | Dibuang (C1) |
| Dropoff Juli di file Juni (899 baris) | `dropoff > 2026-06-30` | Kejadian nyata (perjalanan lewat tengah malam) | Dibiarkan, pickup tetap di Juni |
| Zona Unknown (264/265) | `PULocationID`/`DOLocationID` di luar 1–263 | Lokasi tidak diketahui | Dibuang (C4/C5) |
| Duplikat penuh | `DataFrame.duplicated()` | Tidak ditemukan (0 baris) | Tidak ada yang dibuang (C6 = 0) |
| Kode kategori asing | `value_counts` VendorID/RatecodeID/payment_type | Tidak ditemukan (0 baris) | Tidak ada yang dibuang (C10 = 0) |
| Jarak nol (`trip_distance` == 0) | Hitung `trip_distance == 0` | Bisa kejadian nyata (perjalanan sangat pendek) | Dibiarkan |

---

## 5. Unit Analisis & Agregasi

| Item              | Keputusan                                                                       | Status |
| :---------------- | :------------------------------------------------------------------------------ | :----: |
| Unit analisis     | Zona pickup (pasangan `PU_longitude`, `PU_latitude`) × 1 jam                    | Final  |
| Pembulatan waktu  | `tpep_pickup_datetime` dibulatkan ke jam (waktu lokal NY)                       | Final  |
| Grid zona-jam     | Lengkap; kombinasi tanpa pickup pada jam valid diisi **0**                      | Final  |
| DST               | Mulai **8 Maret 2026**; jam yang tidak ada ditandai **tidak tersedia**, bukan 0 | Final  |
| Dataset turunan   | `main_trips`, `demand_zone_hour`, `revenue_analysis` (opsional)                 | Final  |
| Validasi agregasi | Total pickup di `demand_zone_hour` = jumlah pickup valid di `main_trips`        | Final  |

---

## 6. Analisis Spasial

| Item                           | Keputusan                                                                               | Status |
| :----------------------------- | :-------------------------------------------------------------------------------------- | :----: |
| Autokorelasi global            | Global Moran's I                                                                        | Final  |
| Hotspot / cold spot lokal      | Getis-Ord Gi\*                                                                          | Final  |
| Variabel yang diuji            | ☑ Rata-rata pickup per jam per zona per bulan (dinormalisasi jumlah jam valid; Feb 28 hari, Mar ada jam DST hilang) | Draft  |
| _Spatial weights_              | ☑ KNN (k = 8) pada centroid zona (EPSG:2263); cek sensitivitas k = 6 dan 10. Queen/Rook ditolak: 6 zona island (ID 1, 46, 103, 104, 105, 202) | Draft  |
| Penanganan zona tanpa tetangga | Tidak ada island pada KNN. Zona 264 dan 265 keluar dari analisis spasial karena tidak ada di shapefile | Draft  |
| Koreksi uji berganda           | FDR Benjamini-Hochberg (α = 0,05); 999 permutasi; seed 42 (`np.random.seed(42)` untuk Moran, `seed=42` untuk Gi\*) | Draft  |
| Kriteria hotspot / cold spot   | p-value terkoreksi FDR < 0,05 dan `Zs` > 0 = hotspot; `Zs` < 0 = cold spot (cek `p_sim` satu/dua sisi di notebook) | Draft  |
| Stabilitas antarbulan          | Jaccard Index antar pasangan bulan                                                      | Final  |
| Library                        | `geopandas` 1.2.0, `libpysal` 4.15.1, `esda` 2.10.0, `statsmodels` 0.15.0 (samakan dengan `requirements.txt`) | Draft  |

---

## 7. Fitur & Target

### 7.1 Fitur

| Kelompok           | Fitur                                                      | Tersedia saat waktu prediksi? | Status |
| :----------------- | :--------------------------------------------------------- | :---------------------------: | :----: |
| Waktu              | `hour`, `day_of_week`, `month`, `is_weekend`, `is_holiday`, `is_major_nyc_event` |              Ya               | Final  |
| Historis           | `lag_1`, `lag_24`, `lag_168` (per zona)                    |              Ya               | Draft  |
| Ringkasan historis | Rolling mean 24 jam & 168 jam (sudah di-_shift_)           |              Ya               | Draft  |
| Lokasi             | `PU_longitude`, `PU_latitude`                              |              Ya               | Draft  |
| Atribut zona       | `borough`, `is_airport`, `is_cbd`                          |              Ya               | Draft  |
| Fitur tambahan     | `is_major_nyc_event` (event besar NYC)                    |              Ya               | Final  |

### 7.2 Fitur yang Dilarang (_leakage_)

- Koordinat **dropoff** (tujuan belum diketahui saat armada menunggu penumpang).
- Nilai transaksi pasca-perjalanan: `total_amount`, `fare_amount`, `tip_amount`, `cbd_congestion_fee`.
- Lag/rolling yang tidak di-_shift_.
- _Scaler_ atau batas kelas yang dihitung dari data validation/test.

### 7.3 Target

| Model              | Target (y)                                             | Status |
| :----------------- | :----------------------------------------------------- | :----: |
| Regression         | `pickup_count` pada jam t+1                            | Final  |
| SVM Classification | `demand_level` pada jam t+1 (Rendah / Sedang / Tinggi) | Final  |
| Time Series        | Deret `pickup_count` (kota keseluruhan + Top-K zona)   | Final  |
| Horizon 24 jam     | Pengembangan opsional                                  | Draft  |

### 7.4 Definisi `demand_level`

- Metode batas kelas: ☐ Persentil 33/66 · ☐ Persentil 25/75 · ☐ Relatif terhadap rata-rata historis zona · ☐ \_\_\_\_
- Batas dihitung **hanya dari data training**, lalu dipakai ulang di validation dan test.
- Nilai batas: \_\_\_\_
- Distribusi kelas pada training: \_\_\_\_

### 7.5 Transformasi Target

- Distribusi target (proporsi nol, kemiringan, _outlier_) dari EDA: \_\_\_\_
- Transformasi `log1p`: ☐ Dipakai · ☐ Tidak — alasan: \_\_\_\_ (metrik tetap dihitung pada skala asli)

### 7.6 Kamus Fitur

Lihat `docs/feature_dictionary.md`.

---

## 8. Pembagian Data

| Bagian     | Periode              | Fungsi                             | Status |
| :--------- | :------------------- | :--------------------------------- | :----: |
| Training   | Januari - April 2026 | Melatih model                      | Final  |
| Validation | Mei 2026             | Memilih fitur dan hyperparameter   | Final  |
| Testing    | Juni 2026            | Evaluasi akhir, **dipakai sekali** | Final  |

- Split kronologis; tidak ada _random split_ atau k-fold acak.
- Pengecekan hari libur di tiap bagian: Train (New Year, MLK, Presidents' Day), Validation (Memorial Day, Mother's Day, Fleet Week), Test (Juneteenth, Father's Day, Pride March).
- Kalender libur & event: `datasets/processed/nyc_holiday_event_calendar_2026.csv` (sumber: `FederalHolidays_Event.md`, diolah Anggota 4).

---

## 9. Baseline, Model & Metrik

### 9.1 Baseline

| Baseline                                    | Untuk                   | Status |
| :------------------------------------------ | :---------------------- | :----: |
| Seasonal Naive (lag 168 jam)                | Regresi dan time series | Final  |
| Kelas mayoritas / kelas berdasarkan lag 168 | Klasifikasi             | Final  |

### 9.2 Model

| Kode | Model                   | Materi | Target               | Penanggung jawab | Catatan penting                                     |
| :--- | :---------------------- | :----: | :------------------- | :--------------- | :-------------------------------------------------- |
| 6B   | Linear, Ridge, Lasso    |  P11   | `pickup_count`       | \_\_\_\_         | Opsional: Polynomial / LightGBM                     |
| 6C   | SVM linear dan RBF      |  P10   | `demand_level`       | \_\_\_\_         | `class_weight="balanced"` bila kelas tidak seimbang |
| 6D   | Holt-Winters dan SARIMA |  P12   | Deret `pickup_count` | Aushaf Fathin I N | Periode musiman: ☑ 24 jam (deret per jam) · ☐ Harian (7)            |

### 9.3 Strategi Skala Komputasi

- SVM: ☐ Sampel berurutan waktu dari training · ☐ Top-K zona · ☐ Kernel linear saja
  - Ukuran sampel: \_**\_ · Alasan: \_\_** · Seed: \_\_\_\_
- Time series: K (Top-K zona) = 5 · Kriteria pemilihan Top-K: total pickup periode **training (Jan–Apr) saja**, agar tidak ada kebocoran dari validation/test

### 9.4 Metrik

| Jenis                 | Metrik                                                  | Metrik utama | Catatan                                                        |
| :-------------------- | :------------------------------------------------------ | :----------- | :------------------------------------------------------------- |
| Regresi / Time Series | MAE, RMSE, WAPE, MASE (+ R² untuk regresi)              | \_\_\_\_     | Hindari MAPE (banyak nilai aktual nol); hitung pada skala asli |
| Klasifikasi           | Accuracy, precision, recall, macro-F1, confusion matrix | macro-F1     | —                                                              |
| Pelaporan tambahan    | Metrik terpisah zona ramai vs sepi                      | —            | Definisi "ramai/sepi": \_\_\_\_                                |

### 9.5 Daftar Eksperimen

| ID  | Eksperimen | Hipotesis | Model | Fitur | Metrik | Status |
| :-- | :--------- | :-------- | :---- | :---- | :----- | :----: |
| E1  |            |           |       |       |        |   ☐    |
| E2  |            |           |       |       |        |   ☐    |
| E3  |            |           |       |       |        |   ☐    |

---

## 10. Optimasi & Trade-off (Fase 7)

### 10.1 Hyperparameter Tuning

| Model         | Parameter            | Rentang yang dicoba | Cara                   | Skema validasi                                              |
| :------------ | :------------------- | :------------------ | :--------------------- | :---------------------------------------------------------- |
| Ridge / Lasso | `alpha`              | \_\_\_\_            | Grid search            | `TimeSeriesSplit` (_expanding window_), n_splits = \_\_\_\_ |
| SVM           | `C`, `gamma`, kernel | \_\_\_\_            | Grid / random search   | `TimeSeriesSplit`                                           |
| SARIMA        | (p,d,q)(P,D,Q)       | \_\_\_\_            | AIC / error validation | —                                                           |
| Holt-Winters  | jenis tren & musiman | \_\_\_\_            | Error validation       | —                                                           |

Data test **tidak** dipakai dalam tuning.

### 10.2 Analisis Trade-off

- [ ] Bias vs variance (efek `alpha`, `C`, `gamma` pada error train vs validation)
- [ ] Akurasi vs kompleksitas
- [ ] Akurasi vs waktu (training dan prediksi)
- [ ] Precision vs recall (ambang kelas _Tinggi_)
- [ ] Interpretabilitas vs performa

### 10.3 Optimasi Keputusan: coverage@K _(RQ4)_

- Definisi: coverage@K = pickup aktual di K zona terpilih ÷ total pickup aktual (per jam, lalu dirata-ratakan).
- Nilai K yang diuji: \_\_\_\_
- Pembanding: pemilihan zona berdasarkan baseline.

### 10.4 Kriteria Pemilihan Model Akhir

- Pemilihan memakai **data validation**; evaluasi test dijalankan **sekali** setelah model diumumkan.
- Bobot pertimbangan (urutkan): ☐ Akurasi · ☐ Kompleksitas · ☐ Waktu · ☐ Interpretabilitas
- Syarat dinyatakan lebih baik dari baseline: \_\_\_\_

---

## 11. Struktur Folder & Penyimpanan

| Jenis file                                     | Lokasi               |        Boleh diubah?        |
| :--------------------------------------------- | :------------------- | :-------------------------: |
| Data sumber asli (masih ber-ID)                | `datasets/raw/`      |             ❌              |
| Hasil cleaning, ganti ID → koordinat, agregasi | `datasets/interim/`  |             ✅              |
| Taxi Zone Lookup, Shapefile, tabel centroid    | `datasets/zone/`     | Sumber ❌ · tabel olahan ✅ |
| Kalender libur, data referensi lain            | `datasets/external/` |             ✅              |
| Grafik, tabel, peta, hasil model               | `out/`               |             ✅              |
| Notebook analisis (bernomor)                   | `script/`            |             ✅              |
| Analysis plan & catatan keputusan              | `docs/`              |             ✅              |

**Notebook:** `01_audit` · `02_cleaning_join_coordinates` · `03_eda` · `04a_aggregation` · `04b_spatial_analysis` · `05_features` · `06_regression` · `07_svm_classification` · `08_time_series` · `09_optimization_tradeoff`

**Environment:** Python \_**\_ · pandas \_\_** · numpy \_**\_ · scipy \_\_** · scikit-learn \_**\_ · statsmodels \_\_** · geopandas \_**\_ · libpysal / esda \_\_** (lihat `requirements.txt`)

---

## 12. Risiko & Mitigasi (Pantauan Tim)

| Risiko                                    | Mitigasi                                                    | Status |
| :---------------------------------------- | :---------------------------------------------------------- | :----: |
| Koordinat dianggap GPS asli               | Beri label "centroid zona" di semua visual dan dokumen      |   ☐    |
| Join koordinat menggandakan baris         | Cek jumlah baris sebelum dan sesudah join                   |   ☐    |
| Zona _Unknown_ tidak punya koordinat      | Putuskan di C4/C5; catat di _attrition_                     |   ☐    |
| Data demand terhapus karena anomali tarif | Jalur demand dan revenue dipisah                            |   ☐    |
| Banyak zona-jam bernilai nol              | Grid lengkap; bedakan nol aktual vs jam tidak tersedia      |   ☐    |
| Kesalahan DST                             | Periksa jam lokal NY; tandai 8 Maret 2026                   |   ☐    |
| _Data leakage_                            | Fitur di-_shift_; scaler dan batas kelas dari training saja |   ☐    |
| SVM terlalu lambat                        | Lihat strategi di 9.3                                       |   ☐    |
| SARIMA terlalu berat pada periode 168     | Periode 24 atau agregasi harian                             |   ☐    |
| Model hanya bagus di zona ramai           | Laporkan metrik zona ramai dan sepi                         |   ☐    |
| Terlalu banyak hotspot signifikan         | Koreksi FDR dan laporkan kriteria                           |   ☐    |
| Data 2016 dan 2026 dicampur               | Perlakukan terpisah                                         |   ☐    |

---

## 13. Gate per Fase (Tanda Selesai)

| Fase | Syarat gate                                                                                    | Selesai | Diperiksa oleh | Tanggal |
| :--: | :--------------------------------------------------------------------------------------------- | :-----: | :------------- | :------ |
|  0   | Target, periode, aturan koordinat, dan skema evaluasi sudah ditentukan                         |    ☐    |                |         |
|  1   | Skema keenam file dipahami; perbedaan kolom antarbulan dicatat                                 |    ☐    |                |         |
|  2   | Baris setelah join konsisten; koordinat unik; kegagalan join dicatat; tabel pemetaan tersimpan |    ☐    |                |         |
|  3   | Setiap visual punya penjelasan dan menjawab salah satu RQ                                      |    ☐    |                |         |
|  4   | Total pickup agregat = sumber; grid waktu dan hasil uji spasial diperiksa                      |    ☐    |                |         |
|  5   | Fitur tersedia saat prediksi; tanpa leakage; split benar; batas kelas dari training            |    ☐    |                |         |
|  6   | Semua model dibandingkan dengan baseline pada periode yang sama                                |    ☐    |                |         |
|  7   | Model dipilih dari validation; test dipakai sekali; trade-off dijelaskan                       |    ☐    |                |         |

---

## 14. Log Perubahan Keputusan

Catat **setiap** perubahan keputusan di sini, termasuk perubahan seed, periode, dan aturan cleaning. Jangan mengubah aturan hanya karena hasil awal tidak sesuai harapan.

| No. | Tanggal | Bagian yang diubah | Keputusan lama | Keputusan baru | Alasan (berdasarkan bukti, bukan hasil model) | Diputuskan oleh | Dampak ke fase lain |
| :-: | :------ | :----------------- | :------------- | :------------- | :-------------------------------------------- | :-------------- | :------------------ |
|  1  | 22 Nov 2026 | 6 (Analisis Spasial), 9.2 (6D), 9.3 | Kosong / Draft | KNN k=8; rata-rata pickup/jam/bulan; FDR-BH α=0,05; periode musiman 24 jam; Top-K=5 dari training | Queen/Rook punya 6 island (uji pada taxi_zones.shp); bulan berbeda panjang; Top-K dari training mencegah leakage | Aushaf Fathin I N (menunggu review tim) | Fase 4B, 6D, 7 (tuning TS) |
|  2  |         |                    |                |                |                                               |                 |                     |
|  3  |         |                    |                |                |                                               |                 |                     |

---

## 15. Pertanyaan Terbuka

| No. | Pertanyaan                                                                    | Pemilik  | Batas waktu | Jawaban |
| :-: | :---------------------------------------------------------------------------- | :------- | :---------- | :------ |
|  1  | Materi P12 (Time Series) belum terlihat; apakah langkah 6D perlu disesuaikan? | \_\_\_\_ | \_\_\_\_    |         |
|  2  |                                                                               |          |             |         |
