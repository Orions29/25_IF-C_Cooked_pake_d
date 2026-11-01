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
| **Anggota tim**                  | Rio Meidi A, Anggota 2 , Anggota 3 , Anggota 4 |
| **Seed global (`random_state`)** | 42                                             |

---

## 1. Tujuan & Pertanyaan Penelitian

**Tujuan:** memahami pola pickup taksi kuning, menemukan hotspot, dan memodelkan permintaan per zona per jam.

| Kode | Pertanyaan                                                                                           | Dijawab di    | Penanggung jawab | Status jawaban |
| :--: | :--------------------------------------------------------------------------------------------------- | :------------ | :--------------- | :------------- |
| RQ1  | Bagaimana pola pickup berdasarkan jam, hari, dan bulan?                                              | Fase 3        | \_\_\_\_         | [ ]            |
| RQ2  | Zona mana yang menjadi hotspot / cold spot, dan apakah stabil antarbulan?                            | Fase 4B       | \_\_\_\_         | [ ]            |
| RQ3  | Seberapa akurat model memprediksi pickup per zona per jam, dan model mana yang paling layak dipilih? | Fase 6, 7     | \_\_\_\_         | [ ]            |
| RQ4  | Zona dan waktu mana yang layak diprioritaskan berdasarkan volume pickup?                             | Fase 3, 4B, 7 | \_\_\_\_         | [ ]            |

**Catatan interpretasi:** jumlah pickup adalah _served demand_ (perjalanan yang berhasil dilayani), bukan seluruh permintaan taksi yang sebenarnya.

**Batas ruang lingkup:** pekerjaan berakhir di Fase 7 (Optimasi & Trade-off). Laporan akhir dan rekomendasi operasional di luar dokumen ini.

---

## 2. Dataset & Periode

| Item                | Keputusan                                                            | Status |
| :------------------ | :------------------------------------------------------------------- | :----: |
| Sumber              | NYC TLC, Yellow Taxi Trip Records                                    | Final  |
| Dataset utama       | **2026**                                                             | Final  |
| Periode             | **Januari - Juni 2026** (6 file Parquet)                             | Final  |
| Data 2016 (Jan-Mar) | ☐ Tidak dipakai · ☐ Pembanding terpisah (tidak digabung dengan 2026) | Draft  |
| Zona waktu          | Waktu lokal New York                                                 | Final  |

### 2.1 Inventaris File _(diisi setelah Fase 1)_

| Bulan     | Nama file | Ukuran | Jumlah baris | Jumlah kolom | Rentang pickup (min - maks) | Catatan |
| :-------- | :-------- | -----: | -----------: | -----------: | :-------------------------- | :------ |
| Jan       |           |        |              |              |                             |         |
| Feb       |           |        |              |              |                             |         |
| Mar       |           |        |              |              |                             |         |
| Apr       |           |        |              |              |                             |         |
| Mei       |           |        |              |              |                             |         |
| Jun       |           |        |              |              |                             |         |
| **Total** |           |        |              |              |                             |         |

### 2.2 Temuan Skema _(diisi setelah Fase 1)_

- Konsistensi nama kolom dan tipe data antarbulan: \_\_\_\_
- Kolom yang kosong seluruhnya / hanya ada pada bulan tertentu: \_\_\_\_
- Status kolom `request_source` (ada / tidak): \_\_\_\_
- Apakah dataset 2026 sesuai tujuan penelitian: \_**\_ (alasan: \_\_**)

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
| Perlakuan zona _Unknown_ (ID 264, 265) | ☐ Dibuang · ☐ Dilabeli khusus — alasan: \_\_\_\_                                                                                 | Draft  |
| Definisi `is_airport`                  | \_\_\_\_ (zona mana saja, mis. JFK, LGA)                                                                                         | Draft  |
| Definisi `is_cbd`                      | \_\_\_\_ (zona mana saja)                                                                                                        | Draft  |

**Hasil pemeriksaan tabel centroid** _(diisi setelah Fase 2B)_

- [ ] Satu zona = satu record
- [ ] Pasangan koordinat unik per zona
- [ ] Semua koordinat berada di wilayah NYC
- [ ] Zona tanpa geometri tercatat: \_\_\_\_
- [ ] Jumlah baris `main_trips` sebelum dan sesudah join sama: \_**\_ / \_\_**

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

| ID  | Aturan                                           | Kolom                                           | Batas / kriteria | Jalur                       | Alasan & bukti distribusi | Status |
| :-- | :----------------------------------------------- | :---------------------------------------------- | :--------------- | :-------------------------- | :------------------------ | :----: |
| C1  | Pickup di luar rentang Jan-Jun 2026              | `tpep_pickup_datetime`                          | \_\_\_\_         | Demand + Revenue            |                           | Draft  |
| C2  | Timestamp kosong / tidak valid                   | `tpep_pickup_datetime`, `tpep_dropoff_datetime` | \_\_\_\_         | Demand + Revenue            |                           | Draft  |
| C3  | Dropoff sebelum pickup / durasi tidak wajar      | durasi = dropoff − pickup                       | \_\_\_\_         | Revenue (Demand?: \_\_\_\_) |                           | Draft  |
| C4  | Zona pickup kosong / di luar daftar / _Unknown_  | `PULocationID`                                  | \_\_\_\_         | Demand + Revenue            |                           | Draft  |
| C5  | Zona dropoff kosong / di luar daftar / _Unknown_ | `DOLocationID`                                  | \_\_\_\_         | Revenue (Demand?: \_\_\_\_) |                           | Draft  |
| C6  | Duplikat seluruh baris                           | seluruh kolom                                   | \_\_\_\_         | Demand + Revenue            |                           | Draft  |
| C7  | `trip_distance` nol / negatif / ekstrem          | `trip_distance`                                 | \_\_\_\_         | Revenue                     |                           | Draft  |
| C8  | `fare_amount`, `total_amount` negatif / ekstrem  | `fare_amount`, `total_amount`                   | \_\_\_\_         | Revenue                     |                           | Draft  |
| C9  | `passenger_count` nol / ekstrem                  | `passenger_count`                               | \_\_\_\_         | Revenue                     |                           | Draft  |
| C10 | Kode kategori tidak dikenal                      | `VendorID`, `RatecodeID`, `payment_type`        | \_\_\_\_         | \_\_\_\_                    |                           | Draft  |
| C11 | \_\_\_\_                                         | \_\_\_\_                                        | \_\_\_\_         | \_\_\_\_                    |                           | Draft  |

### 4.3 Penanganan Missing Values

| Kolom | % kosong | Fungsi kolom | Strategi (buang baris / isi / biarkan / buang kolom) | Alasan |
| :---- | -------: | :----------- | :--------------------------------------------------- | :----- |
|       |          |              |                                                      |        |

Tidak ada baris yang dihapus hanya karena satu kolom pendukung kosong.

### 4.4 Duplikat

- Definisi duplikat: \_\_\_\_
- Hasil pemeriksaan (catatan berulang vs perjalanan berbeda): \_\_\_\_
- Aturan penghapusan: \_\_\_\_

### 4.5 Kolom Wajib untuk Analisis

| Jalur   | Kolom wajib |
| :------ | :---------- |
| Demand  | \_\_\_\_    |
| Revenue | \_\_\_\_    |

### 4.6 Log Cleaning (_attrition_)

Diisi otomatis dari notebook `02_cleaning_join_coordinates.ipynb`. Berkas: `out/output_eda/03_cleaning_log.csv`.

| Aturan    | Baris sebelum | Baris dibuang | Baris sesudah | % dibuang | Konsentrasi pada tanggal/periode tertentu? |
| :-------- | ------------: | ------------: | ------------: | --------: | :----------------------------------------- |
| C1        |               |               |               |           |                                            |
| C2        |               |               |               |           |                                            |
| ...       |               |               |               |           |                                            |
| **Total** |               |               |               |           |                                            |

### 4.7 Anomali & Penanganannya

| Anomali | Cara menemukan | Kesalahan pencatatan atau kejadian nyata? | Keputusan |
| :------ | :------------- | :---------------------------------------- | :-------- |
|         |                |                                           |           |

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
| Variabel yang diuji            | ☐ Total pickup per zona per bulan · ☐ Rata-rata pickup per jam · ☐ \_\_\_\_             | Draft  |
| _Spatial weights_              | ☐ Poligon _contiguity_ (Queen / Rook) · ☐ KNN (k = \_**\_) · ☐ Distance band (\_\_** m) | Draft  |
| Penanganan zona tanpa tetangga | \_\_\_\_                                                                                | Draft  |
| Koreksi uji berganda           | FDR (α = \_\_\_\_)                                                                      | Draft  |
| Kriteria hotspot / cold spot   | \_\_\_\_ (mis. z-score, p-value terkoreksi)                                             | Draft  |
| Stabilitas antarbulan          | Jaccard Index antar pasangan bulan                                                      | Final  |
| Library                        | `geopandas`, `libpysal`, `esda` (versi: \_\_\_\_)                                       | Draft  |

---

## 7. Fitur & Target

### 7.1 Fitur

| Kelompok           | Fitur                                                      | Tersedia saat waktu prediksi? | Status |
| :----------------- | :--------------------------------------------------------- | :---------------------------: | :----: |
| Waktu              | `hour`, `day_of_week`, `month`, `is_weekend`, `is_holiday` |              Ya               | Draft  |
| Historis           | `lag_1`, `lag_24`, `lag_168` (per zona)                    |              Ya               | Draft  |
| Ringkasan historis | Rolling mean 24 jam & 168 jam (sudah di-_shift_)           |              Ya               | Draft  |
| Lokasi             | `PU_longitude`, `PU_latitude`                              |              Ya               | Draft  |
| Atribut zona       | `borough`, `is_airport`, `is_cbd`                          |              Ya               | Draft  |
| Fitur tambahan     | \_\_\_\_                                                   |           \_\_\_\_            | Draft  |

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
- Pengecekan hari libur di tiap bagian: Train (\_\_\_\_), Validation (Memorial Day, Mother's Day), Test (Juneteenth, Father's Day).
- Kalender libur & event: `datasets/external/` (sumber: \_\_\_\_).

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
| 6D   | Holt-Winters dan SARIMA |  P12   | Deret `pickup_count` | \_\_\_\_         | Periode musiman: ☐ 24 jam · ☐ Harian (7)            |

### 9.3 Strategi Skala Komputasi

- SVM: ☐ Sampel berurutan waktu dari training · ☐ Top-K zona · ☐ Kernel linear saja
  - Ukuran sampel: \_**\_ · Alasan: \_\_** · Seed: \_\_\_\_
- Time series: K (Top-K zona) = \_**\_ (rekomendasi awal 5) · Kriteria pemilihan Top-K: \_\_**

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
|  1  |         |                    |                |                |                                               |                 |                     |
|  2  |         |                    |                |                |                                               |                 |                     |
|  3  |         |                    |                |                |                                               |                 |                     |

---

## 15. Pertanyaan Terbuka

| No. | Pertanyaan                                                                    | Pemilik  | Batas waktu | Jawaban |
| :-: | :---------------------------------------------------------------------------- | :------- | :---------- | :------ |
|  1  | Materi P12 (Time Series) belum terlihat; apakah langkah 6D perlu disesuaikan? | \_\_\_\_ | \_\_\_\_    |         |
|  2  |                                                                               |          |             |         |
