# TODO Tim - NYC Yellow Taxi Demand Analytics 2026

Pembagian tugas untuk **4 anggota**, disusun dari `Brief_Project_NYC_Taxi_2026.md` (Fase 0–7) dan `TODO.md` sebelumnya.

> Ganti nama **Anggota 2, 3, dan 4** dengan nama asli. Anggota 1 mengikuti pembagian awal (Rio Meidi A).

---

## 1. Ringkasan Peran

| Anggota             | Peran                            | Fase yang dipegang                   | Menjawab |
| :------------------ | :------------------------------- | :----------------------------------- | :------- |
| **1 - Rio Meidi A** | Data Engineer & Feature Engineer | 0, 1, 2 (termasuk tabel zona), 5, 6A | –        |
| **2 - Mufid Dhamarjati K**      | EDA, Agregasi & Regresi          | 3, 4A, 6B                            | RQ1, RQ4 |
| **3 - [Nama]**      | Analisis Spasial & Time Series   | 4B, 6D                               | RQ2      |
| **4 - Erlan Rifqi Davin D**      | Infrastruktur, SVM & Optimasi    | Persiapan env & kalender, 6C, 7      | RQ3, RQ4 |

**Beban kerja per gelombang**

| Gelombang | Fase  | Anggota 1                               | Anggota 2                        | Anggota 3                         | Anggota 4                              |
| :-------: | :---- | :-------------------------------------- | :------------------------------- | :-------------------------------- | :------------------------------------- |
|     A     | 0 – 2 | Plan, audit, tabel zona, cleaning, join | Prototipe notebook EDA (1 bulan) | Siapkan spatial weights & library | Env, folder, kalender libur            |
|     B     | 3 – 4 | Review & dukung                         | EDA + `demand_zone_hour`         | Moran's I, Gi\*, FDR, Jaccard     | Siapkan notebook SVM & protokol tuning |
|     C     | 5     | Fitur, target, split, baseline          | Siapkan notebook regresi         | Siapkan deret waktu 6D            | Siapkan notebook SVM                   |
|     D     | 6     | Review leakage                          | Regresi (6B)                     | Time series (6D)                  | SVM (6C)                               |
|     E     | 7     | Dokumentasi metodologi final            | Tuning Ridge/Lasso               | Tuning SARIMA/Holt-Winters        | Tuning SVM + trade-off + coverage@K    |

---

## 2. Alur Serah-Terima (Dependency)

| Dari            | Ke              | Artefak                                                     | Lokasi                                    |
| :-------------- | :-------------- | :---------------------------------------------------------- | :---------------------------------------- |
| Anggota 1       | Anggota 2, 3    | `zone_centroid_lookup.csv` (dibuat sendiri, tanpa menunggu) | `datasets/zone/`                          |
| Anggota 4       | Anggota 1, 2    | Kalender libur & event 2026 (`is_holiday`)                  | `datasets/external/`                      |
| Anggota 1       | Anggota 2, 3    | `main_trips` + tabel _attrition_                            | `datasets/interim/2026/`                  |
| Anggota 2       | Anggota 1, 3    | `demand_zone_hour` (grid lengkap, DST ditandai)             | `datasets/interim/2026/`                  |
| Anggota 1       | Anggota 2, 3, 4 | Dataset fitur+target, deret waktu, baseline, `metrics.py`   | `datasets/interim/2026/`, `script/tools/` |
| Anggota 2, 3, 4 | Anggota 4       | Hasil tuning + waktu training/prediksi tiap model           | `out/`                                    |

> **Anggota 1 tidak menunggu siapa pun sampai Fase 2 selesai.** Audit, tabel zona, cleaning, dan join semuanya dikerjakan sendiri. Satu-satunya masukan dari luar baru dibutuhkan di Fase 5: `demand_zone_hour` (Anggota 2) dan kalender libur (Anggota 4).

> **Mulai lebih awal tanpa menunggu:** Anggota 2 dan 3 tidak perlu menunggu `main_trips` final. Mereka bisa membuat prototipe notebook memakai **satu bulan data** (misalnya Januari) lalu menjalankannya ulang pada data final.

---

## 3. Aturan Bersama (Semua Anggota)

- [ ] Satu nilai `random_state` / seed global, dicatat di `docs/analysis_plan.md`, dipakai semua notebook.
- [ ] Jangan ubah `datasets/raw/`. ID lokasi hanya dilepas pada salinan di `datasets/interim/`.
- [ ] Split **kronologis**: Train Jan–Apr · Validation Mei · Test Juni. Dilarang random split / k-fold acak.
- [ ] Fitur hanya dari informasi yang tersedia sebelum waktu prediksi. Koordinat dropoff dan nilai biaya pasca-perjalanan tidak dipakai.
- [ ] Jam yang hilang karena DST (8 Maret 2026) = **tidak tersedia**, bukan nol.
- [ ] **Data test dipakai sekali**, setelah model final dipilih Anggota 4.
- [ ] Semua model memakai fungsi metrik yang sama dari `script/tools/metrics.py` (MAE, RMSE, WAPE, MASE, R², macro-F1).
- [ ] Catat **waktu training dan waktu prediksi** setiap model (dipakai di tabel trade-off Fase 7).
- [ ] Setiap perubahan keputusan dicatat di `docs/analysis_plan.md` beserta alasannya. Jangan mengubah aturan hanya karena hasil awal kurang bagus.
- [ ] Gunakan branch Git per anggota; cek silang (_review_) sebelum merge.

---

# 4. TODO per Anggota

---

## 👤 Anggota 1 - Rio Meidi A · Data Engineer & Feature Engineer

**Fase:** 0, 1, 2 (audit, cleaning, tabel zona, join), 5, 6A

### 4.1 Fase 0 - Persiapan & Analysis Plan

- [ ] Menetapkan RQ1–RQ4 dan target penelitian (jumlah pickup 1 jam ke depan).
- [ ] Menetapkan periode **Januari – Juni 2026**.
- [ ] Menuliskan aturan cleaning dan aturan penggantian ID → koordinat **sebelum** diterapkan.
- [ ] Menetapkan metode hotspot (Moran's I + Getis-Ord Gi\*) dan skema split data bersama Anggota 3.
- [ ] Mencatat seed, periode, dan semua keputusan di `docs/analysis_plan.md`.

**Output:** `docs/analysis_plan.md`
**Gate:** target, periode, aturan koordinat, dan skema evaluasi sudah ditentukan.

### 4.2 Fase 1 - Audit Dataset (6 file Parquet)

- [ ] Memastikan keenam bulan (Jan–Jun 2026) tersedia dan lengkap.
- [ ] Mencatat ukuran file, jumlah baris, dan jumlah kolom tiap file.
- [ ] Membandingkan nama kolom dan tipe data antarbulan; mencatat kolom yang kosong seluruhnya atau hanya ada di bulan tertentu.
- [ ] Memeriksa apakah kolom `request_source` ada, lalu menyesuaikan data dictionary dengan skema asli.
- [ ] Memeriksa rentang `tpep_pickup_datetime` dan `tpep_dropoff_datetime`, termasuk timestamp di luar Jan–Jun 2026.
- [ ] Menghitung jumlah dan persentase _missing values_ per kolom.
- [ ] Menghitung duplikat seluruh baris dan memeriksa apakah itu catatan berulang atau perjalanan berbeda.
- [ ] Memeriksa nilai tidak wajar: `trip_distance`, `fare_amount`, `total_amount`, `passenger_count`, durasi negatif/ekstrem.
- [ ] Memeriksa kode `VendorID`, `RatecodeID`, `payment_type` dan ID lokasi di luar daftar zona.
- [ ] Menyimpulkan apakah dataset 2026 sesuai tujuan penelitian.

**Output** (di `out/output_eda/`): `00_file_inventory.csv`, `01_schema_comparison.csv`, `02_data_quality.csv`; notebook `script/01_audit.ipynb`
**Gate:** skema keenam file dipahami dan perbedaan kolom antarbulan sudah dicatat.

### 4.3 Fase 2A - Cleaning

- [ ] Menetapkan kolom wajib untuk analisis demand (waktu dan lokasi pickup valid).
- [ ] **Memisahkan aturan demand dan aturan revenue**: baris dengan tarif/jarak bermasalah tidak otomatis dibuang dari analisis demand.
- [ ] Menandai nilai ekstrem dan memeriksa distribusinya sebelum memutuskan dibuang; mendokumentasikan batas dan alasan tiap aturan.
- [ ] Menentukan aturan duplikat dan jumlah baris yang dihapus.
- [ ] Memeriksa durasi negatif/tidak masuk akal dan timestamp di luar rentang; membedakan kesalahan pencatatan dari kejadian nyata.
- [ ] Menentukan nasib zona _Unknown_ (umumnya ID 264 dan 265): dibuang atau dilabeli khusus.
- [ ] Menerapkan aturan satu per satu dan mencatat baris sebelum/dibuang/sesudah serta persentasenya.
- [ ] Memeriksa apakah penghapusan terkonsentrasi pada tanggal atau periode tertentu.

**Template log (`03_cleaning_log.csv`):**

| Aturan                       | Baris sebelum | Baris dibuang | Baris sesudah | % dibuang | Alasan |
| :--------------------------- | ------------: | ------------: | ------------: | --------: | :----- |
| Data di luar rentang waktu   |               |               |               |           |        |
| Timestamp tidak valid        |               |               |               |           |        |
| Missing values sesuai aturan |               |               |               |           |        |
| Duplikat seluruh baris       |               |               |               |           |        |
| Nilai perjalanan tidak valid |               |               |               |           |        |
| Zona _Unknown_               |               |               |               |           |        |
| Aturan lainnya               |               |               |               |           |        |

### 4.4 Fase 2B - Tabel Zona & Join Koordinat

**Tabel zona (dikerjakan sendiri, bisa paralel dengan audit)**

- [ ] Mengunduh Taxi Zone Lookup dan Shapefile TLC ke `datasets/zone/`.
- [ ] Menghitung centroid tiap zona **sekali** dalam WGS84 (EPSG:4326) menjadi satu tabel; jangan dihitung ulang per file.
- [ ] Membuat `zone_centroid_lookup.csv` berisi `LocationID`, `longitude`, `latitude`, `zone_name`, `borough`, `is_airport`, `is_cbd`.
- [ ] Memastikan satu zona = satu record dan pasangan koordinat **unik** per zona.
- [ ] Mencatat zona tanpa geometri (umumnya ID 264 dan 265) dan koordinat di luar wilayah NYC.
- [ ] Menjelaskan di dokumentasi bahwa koordinat adalah **centroid zona**, bukan GPS asli.

**Join ke data perjalanan**

- [ ] Menurunkan atribut zona (`borough`, `is_airport`, `is_cbd`) **sebelum** ID dilepas.
- [ ] _Left join_ ke `PULocationID` → `PU_longitude`/`PU_latitude` dan `DOLocationID` → `DO_longitude`/`DO_latitude`.
- [ ] Memastikan jumlah baris **tidak bertambah** setelah join.
- [ ] Menangani koordinat kosong dan mencatat kegagalan join di tabel _attrition_.
- [ ] Memastikan koordinat berada di wilayah NYC dan unik per zona.
- [ ] Melepas `PULocationID` dan `DOLocationID` dari `main_trips` (hanya di `interim/`).
- [ ] Menyimpan `main_trips`; opsional `revenue_analysis` bila dibutuhkan.

**Output:** `main_trips`, tabel _attrition_ (`datasets/interim/2026/`, `out/output_eda/`); notebook `script/02_cleaning_join_coordinates.ipynb`
**Gate:** jumlah baris setelah join konsisten, koordinat unik per zona, kegagalan join tercatat, tabel pemetaan tersimpan.

### 4.5 Fase 5 - Feature Engineering & Persiapan Supervised Learning

_Data final menunggu `demand_zone_hour` dari Anggota 2. Sambil menunggu, buat dan uji pipeline fitur memakai agregasi cepat satu bulan dari `main_trips`, lalu jalankan ulang pada data final._

- [ ] Fitur waktu: `hour`, `day_of_week`, `month`, `is_weekend`, `is_holiday`.
- [ ] Fitur historis per zona: `lag_1`, `lag_24`, `lag_168`.
- [ ] Rolling mean 24 jam dan 168 jam (sudah di-_shift_ agar tidak melihat jam prediksi).
- [ ] Fitur lokasi: `PU_longitude`, `PU_latitude`; atribut zona: `borough`, `is_airport`, `is_cbd`.
- [ ] Target regresi: `pickup_count` jam t+1.
- [ ] Target klasifikasi: `demand_level` (Rendah/Sedang/Tinggi) dengan **batas kelas dari data training saja**.
- [ ] Split kronologis Train/Validation/Test; _scaler_ di-_fit_ hanya pada training.
- [ ] Menyiapkan deret waktu kota keseluruhan dan Top-K zona (K = 5) untuk Anggota 3.
- [ ] Memastikan tidak ada koordinat dropoff dan nilai transaksi pasca-perjalanan di fitur.
- [ ] Menulis `docs/feature_dictionary.md` (nama, tipe, definisi, tujuan, tersedia saat prediksi atau tidak).
- [ ] Menjalankan pemeriksaan _data leakage_ pada setiap fitur.

**Output:** dataset fitur+target, deret waktu, `docs/feature_dictionary.md`; notebook `script/05_features.ipynb`
**Gate:** setiap fitur tersedia saat waktu prediksi, tidak ada leakage, split benar, batas kelas hanya dari training.

### 4.6 Fase 6A - Baseline

- [ ] Membuat `script/tools/metrics.py` (MAE, RMSE, WAPE, MASE, R², macro-F1) untuk dipakai seluruh tim.
- [ ] Menghitung baseline **Seasonal Naive (lag 168)** pada validation dan test.
- [ ] Membuat baseline klasifikasi: kelas mayoritas dan kelas berdasarkan lag 168.
- [ ] Menyimpan prediksi baseline agar semua model dibandingkan pada periode yang sama.

### 4.7 Fase 7 - Dukungan

- [ ] Merangkum metodologi final dan seluruh perubahan keputusan di `docs/analysis_plan.md`.
- [ ] Memeriksa ulang leakage pada model akhir sebelum evaluasi test.

---

## 👤 Mufid Dhamarjati K- [Nama] · EDA, Agregasi & Regresi

**Fase:** 3, 4A, 6B

### 4.8 Fase 3 - EDA _(RQ1, RQ4)_

_Prototipe boleh dimulai dengan satu bulan data; jalankan ulang pada `main_trips` final._

- [ ] Menghitung jumlah perjalanan per bulan.
- [ ] Grafik pickup per jam, per hari, dan per bulan.
- [ ] Membandingkan hari kerja, akhir pekan, dan hari libur (kalender dari Anggota 4).
- [ ] Menganalisis zona dengan pickup terbanyak dan konsentrasi Top-K.
- [ ] Distribusi pickup per borough.
- [ ] Distribusi jarak, durasi, dan tarif perjalanan.
- [ ] Peta persebaran pickup berdasarkan centroid zona (simpan HTML di `out/html/`).
- [ ] Pola asal-tujuan memakai koordinat pickup dan dropoff.
- [ ] Analisis `cbd_congestion_fee` secara **deskriptif saja**, tidak untuk menyimpulkan dampak kausal.
- [ ] Membandingkan distribusi sebelum dan sesudah cleaning.
- [ ] Mengecek distribusi target: proporsi nol, kemiringan, _outlier_ (menentukan transformasi dan metrik di Fase 6).
- [ ] Memeriksa ulang angka ringkasan dan uji statistik EDA UTS sebelum dipakai sebagai kesimpulan.
- [ ] Mencatat temuan utama dan pertanyaan lanjutan dari tiap visual.

**Output:** `script/03_eda.ipynb`, grafik/peta/tabel di `out/output_eda/` dan `out/html/`, ringkasan temuan
**Gate:** setiap visual punya penjelasan dan menjawab salah satu RQ.

### 4.9 Fase 4A - Agregasi `demand_zone_hour` _(prioritas, memblokir Anggota 1 dan 3)_

- [ ] Membulatkan `tpep_pickup_datetime` ke interval satu jam (waktu lokal New York).
- [ ] Mengelompokkan berdasarkan pasangan `PU_longitude`/`PU_latitude` dan jam.
- [ ] Membuat **grid zona-jam lengkap**; kombinasi tanpa pickup pada jam valid diisi **nol**.
- [ ] Menandai jam yang tidak ada karena DST (8 Maret 2026) sebagai **tidak tersedia**, bukan nol.
- [ ] Menghubungkan hasil dengan nama zona, borough, dan geometri lewat tabel pemetaan.
- [ ] Memverifikasi total pickup agregat = jumlah pickup valid pada `main_trips`.
- [ ] Menyimpan `demand_zone_hour` di `datasets/interim/2026/`.

**Output:** `demand_zone_hour`; notebook `script/04a_aggregation.ipynb`
**Gate:** total pickup agregat sama dengan sumber; grid waktu sudah diperiksa.

### 4.10 Fase 6B - Regression _(P11)_

> Tugas P11 (Regression) dibuka **5 November 2026**.

- [ ] Melatih Linear Regression, Ridge, dan Lasso untuk `pickup_count` jam t+1.
- [ ] Standardisasi fitur numerik (scaler dari training saja).
- [ ] Bila distribusi sangat miring dan banyak nol, mencoba `log1p` pada target, tetapi **metrik dihitung pada skala asli**.
- [ ] Mengevaluasi MAE, RMSE, R², WAPE, MASE (terhadap seasonal naive). **Hindari MAPE** sebagai metrik utama.
- [ ] Memeriksa asumsi regresi: residual dan multikolinearitas fitur lag.
- [ ] Membandingkan error train vs validation untuk mendeteksi _overfitting_/_underfitting_.
- [ ] Melaporkan metrik terpisah untuk zona ramai dan zona sepi.
- [ ] Menyajikan koefisien terpenting untuk interpretabilitas.
- [ ] Opsional: Polynomial / LightGBM sebagai pembanding bila waktu memungkinkan.
- [ ] Mencatat waktu training dan prediksi.

**Output:** `script/06_regression.ipynb`, tabel metrik, grafik aktual vs prediksi, analisis kesalahan (`out/`)

### 4.11 Fase 7 - Tuning Regresi

- [ ] Grid search `alpha` untuk Ridge/Lasso dengan `TimeSeriesSplit` (_expanding window_) pada data training.
- [ ] Menyerahkan hasil tuning dan waktu komputasi ke Anggota 4.

---

## 👤 Anggota 3 - [Nama] · Analisis Spasial & Time Series

**Fase:** 4B, 6D

### 4.12 Fase 4B - Analisis Spasial _(RQ2, RQ4)_

_Persiapan (spatial weights, library) bisa dimulai begitu `zone_centroid_lookup.csv` dari Anggota 1 tersedia._

- [ ] Memasang dan menguji `geopandas`, `libpysal`, `esda`.
- [ ] Menentukan _spatial weights_: poligon _contiguity_ atau titik centroid dengan KNN / distance band; mencatat metode dan penanganan zona tanpa tetangga.
- [ ] Menghitung **Global Moran's I** (autokorelasi spasial).
- [ ] Menghitung **Getis-Ord Gi\*** untuk hotspot dan cold spot.
- [ ] Menerapkan koreksi uji berganda (**FDR**) pada hasil uji lokal dan melaporkan kriterianya.
- [ ] Membuat peta hotspot/cold spot (`out/html/`).
- [ ] Membandingkan hotspot antarbulan dengan **Jaccard Index** dan menyimpulkan apakah hotspot stabil.
- [ ] Menjawab RQ2 dan memberi masukan untuk RQ4 (zona prioritas).

**Output:** peta hotspot/cold spot, hasil Moran's I dan Gi\*, tabel stabilitas bulanan; notebook `script/04b_spatial_analysis.ipynb`
**Gate:** hasil uji spasial sudah diperiksa; metode weights dan koreksi FDR tercatat.

### 4.13 Fase 6D - Time Series Analysis _(P12)_

> Materi P12 belum terlihat di halaman kuliah; sesuaikan langkah dengan materi dosen bila sudah tersedia.

- [ ] Memodelkan deret **kota keseluruhan** dan **Top-K zona** (K = 5).
- [ ] Eksplorasi: plot deret dan dekomposisi **STL** (musiman harian 24 jam / mingguan 168 jam).
- [ ] Uji stasioneritas **ADF**; _differencing_ bila perlu.
- [ ] **ACF/PACF** untuk memilih orde.
- [ ] Melatih **Holt-Winters (ETS)** dan **SARIMA**. Karena periode 168 sangat berat, gunakan periode **24** pada deret per jam atau agregasi **harian** dengan periode 7; catat pilihan yang dipakai.
- [ ] Prediksi Mei (validation) dan Juni (test, hanya setelah model final dipilih); bandingkan dengan seasonal naive.
- [ ] Memeriksa residual (tidak berpola, mendekati _white noise_).
- [ ] Mengevaluasi MAE, RMSE, WAPE, MASE dan mencatat waktu training/prediksi.

**Output:** `script/08_time_series.ipynb`, tabel metrik, grafik aktual vs prediksi (`out/`)

### 4.14 Fase 7 - Tuning Time Series

- [ ] Membandingkan orde SARIMA (p,d,q)(P,D,Q) dengan AIC / error validation.
- [ ] Membandingkan jenis tren dan musiman Holt-Winters dengan error validation.
- [ ] Menyerahkan hasil tuning dan waktu komputasi ke Anggota 4.

---

## 👤 Anggota 4 - [Nama] · Infrastruktur, SVM & Optimasi

**Fase:** Persiapan env & kalender (paralel dengan Fase 0–2), 6C, 7

### 4.15 Persiapan Infrastruktur _(kerjakan paling awal; tidak memblokir Anggota 1)_

- [ ] Membuat virtual environment (`py -m venv .venv`) dan memasang library: pandas, numpy, scipy, matplotlib, seaborn, pyarrow, jupyter, **scikit-learn, statsmodels, geopandas, libpysal, esda**.
- [ ] Membuat `requirements.txt` dengan versi yang dipakai agar notebook dapat dijalankan ulang oleh semua anggota.
- [ ] Menyesuaikan struktur folder dengan brief (`datasets/`, `docs/`, `out/`, `script/`). Folder `datasets/zone/` dipakai Anggota 1.
- [ ] Memindahkan folder `withZone/` ke `datasets/interim/2026/`.
- [ ] Memeriksa `.gitignore` agar file data besar tidak ikut ter-commit.
- [ ] Memperbarui `README.md` (cara setup, urutan notebook, pembagian tugas).

### 4.16 Kalender Libur & Event

- [ ] Menyalin kalender libur/event Jan–Jun 2026 (brief bagian 3.7 / `FederalHolidays_Event.md`) ke `datasets/external/`.
- [ ] Membuat kolom `is_holiday` (dan kategori event) yang siap di-join per tanggal.
- [ ] Memastikan libur ada di tiap bagian split (Train, Validation, Test).

### 4.17 Fase 6C - SVM Classification _(P10)_

- [ ] Melatih SVM kernel **linear** (`LinearSVC`/`SVC`) dan **RBF** untuk `demand_level` jam t+1.
- [ ] Menentukan strategi skala komputasi: sampel yang menjaga urutan waktu (dari periode training), batasi Top-K zona, atau kernel linear. Catat ukuran sampel dan alasannya; tetapkan seed.
- [ ] Standardisasi fitur (scaler dari training saja).
- [ ] Bila kelas tidak seimbang, pakai `class_weight="balanced"`.
- [ ] Mengevaluasi accuracy, precision, recall, **macro-F1** (metrik utama), dan _confusion matrix_.
- [ ] Membandingkan dengan baseline klasifikasi dan memeriksa selisih train vs validation.
- [ ] Mencatat waktu training dan prediksi.

**Output:** `script/07_svm_classification.ipynb`, tabel metrik, confusion matrix (`out/`)

### 4.18 Fase 7 - Optimasi & Trade-off _(P13)_

**A. Tuning**

- [ ] Menetapkan protokol tuning bersama: `TimeSeriesSplit` / _expanding window_ pada data training, tanpa k-fold acak, tanpa menyentuh data test.
- [ ] Tuning SVM: `C`, `gamma`, jenis kernel (grid/random search).
- [ ] Mengumpulkan hasil tuning Anggota 2 (Ridge/Lasso) dan Anggota 3 (SARIMA/Holt-Winters).

**B. Analisis trade-off**

- [ ] Bias vs variance: efek `alpha`, `C`, `gamma` pada error train vs validation.
- [ ] Akurasi vs kompleksitas: model sederhana vs kompleks.
- [ ] Akurasi vs waktu: metrik dibanding waktu training dan prediksi.
- [ ] Precision vs recall: pengaruh ambang kelas _Tinggi_.
- [ ] Interpretabilitas vs performa.
- [ ] Mengisi tabel perbandingan model (metrik utama, waktu training, waktu prediksi, interpretabilitas, catatan).

**C. Optimasi keputusan - coverage@K _(RQ4)_**

- [ ] Untuk tiap jam, memilih K zona dengan prediksi tertinggi.
- [ ] Menghitung coverage@K = pickup aktual di K zona terpilih ÷ total pickup aktual.
- [ ] Memvariasikan K dan membandingkannya dengan pemilihan berdasarkan baseline.
- [ ] Membuat grafik trade-off K vs coverage.

**D. Pemilihan model akhir**

- [ ] Memilih model **berdasarkan data validation** dan menjelaskan alasan dengan trade-off yang jelas.
- [ ] Mengumumkan model final ke tim, lalu menjalankan evaluasi pada data **test hanya satu kali**.
- [ ] Menyatakan model lebih baik dari baseline **hanya jika hasil evaluasi mendukung**.

**Output:** `script/09_optimization_tradeoff.ipynb`, hasil tuning, tabel trade-off, model terpilih beserta alasannya, grafik coverage@K (`out/`)

---

# 5. Keputusan yang Sudah Terkunci di Brief

Mengisi bagian “Catatan Keputusan yang Belum Final” pada TODO sebelumnya. Salin ke `docs/analysis_plan.md` dan ubah hanya bila ada alasan tertulis.

| Keputusan           | Nilai di brief                                                 |
| :------------------ | :------------------------------------------------------------- |
| Dataset final       | **2026** (data 2016 hanya pembanding opsional, tidak digabung) |
| Rentang bulan       | **Januari – Juni 2026** (6 file Parquet)                       |
| Tujuan utama        | Pola pickup, hotspot, dan prediksi permintaan per zona per jam |
| Representasi lokasi | Longitude & latitude **centroid zona** (raw tetap ber-ID)      |
| Unit analisis       | Zona pickup × 1 jam                                            |
| Target              | Jumlah pickup 1 jam ke depan                                   |
| Model               | Linear/Ridge/Lasso, SVM (linear & RBF), Holt-Winters & SARIMA  |
| Baseline            | Seasonal Naive (lag 168 jam)                                   |
| Split               | Train Jan–Apr · Validation Mei · Test Juni                     |
| Metrik regresi/TS   | MAE, RMSE, WAPE, MASE (+ R² untuk regresi)                     |
| Metrik klasifikasi  | macro-F1, precision, recall                                    |

---

# 6. Checklist Akhir Tim

**Data** - Anggota 1 (folder oleh Anggota 4)

- [ ] Enam file Parquet sudah diaudit; skema dan _missing values_ diperiksa.
- [ ] Aturan cleaning dan jumlah baris yang dibuang tercatat.
- [ ] Tabel centroid tersimpan di `datasets/zone/`; atribut zona diturunkan sebelum ID dilepas.
- [ ] `main_trips` memakai koordinat tanpa kolom ID lokasi; koordinat unik per zona.
- [ ] Folder `withZone/` sudah dipindahkan ke `datasets/interim/2026/`.

**Analisis** - Anggota 2 & 3

- [ ] EDA temporal dan spasial selesai.
- [ ] `demand_zone_hour` lengkap; nol dan DST ditangani.
- [ ] Moran's I dan Gi\* dijalankan; stabilitas hotspot dievaluasi.

**Modeling** - Anggota 1, 2, 3, 4

- [ ] Fitur dan target tanpa leakage; split kronologis.
- [ ] Baseline seasonal naive dihitung.
- [ ] Regresi, SVM, dan time series dilatih dan dievaluasi.
- [ ] Hyperparameter tuning memakai validasi berbasis waktu.
- [ ] Tabel trade-off dibuat; model akhir dipilih dari validation dan diuji sekali di test.
- [ ] Analisis coverage@K selesai.

> **Batas brief:** pekerjaan berakhir pada Fase 7 (Optimasi & Trade-off). Laporan akhir dan rekomendasi operasional disusun setelah hasil modeling tersedia.
