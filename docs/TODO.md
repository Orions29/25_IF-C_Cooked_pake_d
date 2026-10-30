# Apa yang Sedang Dilakukan Orang-Orang

## Penjelasan Aktivitas Saat Ini

## [Rio Meidi A] — Apa yang Sedang Dilakukan Sekarang

### 1. Pengecekan Dataset

- [ ] Memeriksa dataset 2026 yang sudah diunduh.
- [ ] Memastikan bulan yang tersedia dan jumlah file. Jika tersedia Januari–Juli, pastikan seluruh tujuh bulan terwakili.
- [ ] Mencatat ukuran file, jumlah baris, dan jumlah kolom setiap file.
- [ ] Memeriksa rentang waktu `tpep_pickup_datetime` dan `tpep_dropoff_datetime`.
- [ ] Mengidentifikasi seluruh fitur yang tersedia pada dataset 2026.
- [ ] Memeriksa apakah nama kolom dan tipe data konsisten antarbulan.
- [ ] Memeriksa kolom yang seluruh nilainya kosong atau hanya tersedia pada bulan tertentu.
- [ ] Menentukan apakah dataset 2026 sesuai dengan tujuan penelitian.

**Output yang diharapkan:**

- `reports/tables/00_file_inventory.csv`
- `reports/tables/01_schema_comparison.csv`
- `analysis_plan.md`

### 2. Dataset Engineering

#### 2.1 Audit Kualitas Dataset

- [ ] **Missing Values**
  - [ ] Menghitung jumlah nilai kosong pada setiap kolom.
  - [ ] Menghitung persentase nilai kosong pada setiap kolom.
  - [ ] Mengidentifikasi kolom yang nilai kosongnya perlu ditangani.
  - [ ] Menentukan strategi penanganan berdasarkan fungsi kolom dan tujuan analisis.
  - [ ] Tidak langsung menghapus baris hanya karena satu kolom memiliki nilai kosong.

- [ ] **Duplicate Values**
  - [ ] Menghitung jumlah duplikat seluruh baris.
  - [ ] Memeriksa apakah duplikat merupakan catatan berulang atau perjalanan berbeda yang kebetulan memiliki nilai serupa.
  - [ ] Menentukan aturan penghapusan duplikat dan mencatat jumlah baris yang dihapus.

- [ ] **Outlier**
  - [ ] Memeriksa distribusi `trip_distance`.
  - [ ] Memeriksa distribusi `fare_amount` dan `total_amount`.
  - [ ] Memeriksa distribusi `passenger_count`.
  - [ ] Memeriksa nilai nol, negatif, atau nilai ekstrem yang tidak masuk akal.
  - [ ] Menandai nilai ekstrem untuk diperiksa sebelum memutuskan apakah perlu dihapus.
  - [ ] Mendokumentasikan batas dan alasan setiap aturan.

- [ ] **Anomaly Detection**
  - [ ] Menghitung jumlah perjalanan per jam dan per hari.
  - [ ] Mengidentifikasi lonjakan atau penurunan jumlah perjalanan yang tidak biasa.
  - [ ] Memeriksa timestamp yang berada di luar periode dataset yang dipilih.
  - [ ] Memeriksa durasi perjalanan yang negatif atau tidak masuk akal.
  - [ ] Membedakan kesalahan pencatatan dari kejadian nyata.
  - [ ] Mendokumentasikan anomali yang ditemukan dan keputusan penanganannya.

- [ ] **Validasi Timestamp**
  - [ ] Memastikan kolom pickup dan dropoff terbaca sebagai tipe datetime.
  - [ ] Memeriksa timestamp kosong atau tidak valid.
  - [ ] Menghitung durasi perjalanan dari waktu pickup dan dropoff.
  - [ ] Memeriksa perjalanan dengan waktu dropoff sebelum waktu pickup.
  - [ ] Memastikan seluruh data berada pada rentang waktu penelitian.

- [ ] **Validasi Nilai dan Kategori**
  - [ ] Memeriksa nilai ID lokasi yang kosong atau tidak dikenal, jika kolom tersedia.
  - [ ] Memeriksa kode kategori seperti `VendorID`, `RatecodeID`, dan `payment_type`.
  - [ ] Memeriksa nilai finansial yang tidak masuk akal.
  - [ ] Memastikan satuan setiap atribut dipahami sebelum dipakai.

**Output yang diharapkan:**

- `reports/tables/02_data_quality.csv`
- `reports/tables/03_cleaning_log.csv`
- Grafik dan catatan hasil pemeriksaan kualitas data.

#### 2.2 Menentukan Aturan Data Cleaning

- [ ] Membuat daftar aturan cleaning sebelum diterapkan.
- [ ] Menentukan kolom yang wajib tersedia untuk analisis.
- [ ] Menentukan penanganan missing values untuk tiap kolom.
- [ ] Menentukan aturan penghapusan duplikat.
- [ ] Menentukan batas nilai tidak valid berdasarkan logika perjalanan dan dokumentasi.
- [ ] Memastikan aturan outlier tidak menghapus perjalanan yang sebenarnya valid.
- [ ] Menyimpan dataset mentah tanpa perubahan di folder `data/raw/`.
- [ ] Menyimpan hasil cleaning secara terpisah di folder `data/interim/` atau `data/processed/`.
- [ ] Mencatat jumlah baris sebelum dan sesudah setiap aturan.
- [ ] Menghitung persentase baris yang dihapus pada setiap langkah.
- [ ] Memeriksa apakah penghapusan data terkonsentrasi pada tanggal atau periode tertentu.

**Template log cleaning:**

| Aturan                       | Baris sebelum | Baris dibuang | Baris sesudah | Alasan |
| ---------------------------- | ------------: | ------------: | ------------: | ------ |
| Data di luar rentang waktu   |               |               |               |        |
| Timestamp tidak valid        |               |               |               |        |
| Missing values sesuai aturan |               |               |               |        |
| Duplikat seluruh baris       |               |               |               |        |
| Nilai perjalanan tidak valid |               |               |               |        |
| Aturan lainnya               |               |               |               |        |

#### 2.3 Penanganan `PULocationID` dan `DOLocationID`

- [ ] Memastikan apakah dataset yang dipilih menggunakan koordinat GPS atau ID zona.
- [ ] Memahami bahwa `PULocationID` merupakan ID zona pickup dan `DOLocationID` merupakan ID zona dropoff.
- [ ] **Tidak mengganti ID zona dengan longitude/latitude secara langsung**, karena ID zona bukan koordinat geografis.
- [ ] Jika dataset 2026 digunakan, memeriksa kebutuhan _Taxi Zone Lookup Table_ untuk memperoleh nama zona dan borough.
- [ ] Jika analisis membutuhkan geometri zona, mengevaluasi penggunaan _Taxi Zone Shapefile_.
- [ ] Jika menggunakan centroid zona, memberi nama kolom yang jelas, misalnya `PU_centroid_longitude`, `PU_centroid_latitude`, `DO_centroid_longitude`, dan `DO_centroid_latitude`.
- [ ] Menjelaskan bahwa centroid hanya mewakili perkiraan pusat zona, bukan lokasi pickup/dropoff GPS yang sebenarnya.
- [ ] Mempertahankan kolom ID zona sebagai referensi untuk analisis perjalanan antarzona.
- [ ] Menetapkan representasi lokasi berdasarkan tujuan clustering dan ketersediaan data.

**Keputusan yang perlu dicatat:**

| Pilihan            | Kapan digunakan                                       | Catatan                                   |
| ------------------ | ----------------------------------------------------- | ----------------------------------------- |
| ID zona            | Analisis pickup/dropoff dan perjalanan antarzona      | Pertahankan ID asli                       |
| Nama zona/borough  | Analisis agregat berdasarkan wilayah                  | Perlu lookup table                        |
| Centroid zona      | Visualisasi atau pendekatan spasial berbasis titik    | Bukan koordinat perjalanan sebenarnya     |
| Koordinat GPS asli | Clustering berdasarkan lokasi perjalanan yang presisi | Hanya jika koordinat benar-benar tersedia |

#### 2.4 Feature Engineering

- [ ] Menentukan fitur yang diperlukan berdasarkan tujuan analisis.
- [ ] Membuat fitur waktu dari `tpep_pickup_datetime`, jika diperlukan:
  - [ ] `pickup_hour`
  - [ ] `day_of_week`
  - [ ] `is_weekend`
  - [ ] `day_index`
- [ ] Menghitung `trip_duration` dari waktu dropoff dikurangi waktu pickup.
- [ ] Memastikan durasi yang tidak valid ditangani sesuai aturan cleaning.
- [ ] Menentukan fitur spasial berdasarkan data yang tersedia: koordinat GPS, ID zona, atau centroid zona.
- [ ] Menentukan fitur target untuk forecasting, misalnya jumlah pickup per jam.
- [ ] Menyusun kamus fitur berisi nama, tipe data, definisi, dan tujuan penggunaan.
- [ ] Menghindari fitur yang tidak relevan atau menyebabkan kebocoran informasi (_data leakage_).

**Output yang diharapkan:** `feature_dictionary.md`

### 3. Exploratory Data Analysis (EDA)

- [ ] Menghitung jumlah perjalanan per bulan.
- [ ] Membuat grafik jumlah perjalanan per jam.
- [ ] Membuat grafik jumlah perjalanan per hari.
- [ ] Membandingkan pola perjalanan pada hari kerja dan akhir pekan.
- [ ] Memeriksa distribusi jarak perjalanan.
- [ ] Memeriksa distribusi durasi perjalanan.
- [ ] Memeriksa distribusi tarif.
- [ ] Menganalisis zona pickup dan dropoff yang paling sering muncul, jika ID zona tersedia.
- [ ] Membuat visualisasi spasial yang sesuai dengan jenis lokasi yang tersedia.
- [ ] Membandingkan distribusi sebelum dan sesudah cleaning.
- [ ] Mencatat temuan utama dan pertanyaan lanjutan dari setiap visualisasi.

**Output yang diharapkan:**

- Notebook EDA.
- Grafik distribusi dan pola waktu.
- Grafik atau peta spasial jika data mendukung.
- Ringkasan temuan awal.

### 4. Persiapan Analisis Lanjutan

- [ ] Menentukan apakah data cocok untuk clustering.
- [ ] Menentukan apakah data cocok untuk forecasting.
- [ ] Menetapkan unit analisis, misalnya perjalanan, zona, atau zona × jam.
- [ ] Menentukan target dan fitur untuk model.
- [ ] Menentukan skema validasi berbasis waktu jika melakukan forecasting.
- [ ] Menyusun daftar eksperimen dan metrik evaluasi.
- [ ] Memastikan keputusan metodologi terdokumentasi sebelum pemodelan.

---

## 5. Struktur Folder yang Disarankan

```text
nyc-taxi-project/
├── README.md
├── analysis_plan.md
├── data/
│   ├── raw/                 # Data asli, tidak diubah
│   ├── interim/             # Data setelah tahap pengolahan antara
│   ├── processed/           # Data bersih yang siap dianalisis
│   └── external/            # Lookup table, shapefile, atau data eksternal
├── notebooks/
│   ├── 01_dataset_inventory.ipynb
│   ├── 02_data_quality_audit.ipynb
│   ├── 03_data_cleaning.ipynb
│   └── 04_eda.ipynb
├── reports/
│   ├── figures/
│   └── tables/
└── docs/
    └── feature_dictionary.md
```

> Sesuaikan struktur folder dengan struktur repositori yang sudah ada. Jangan menggandakan file besar tanpa kebutuhan.

---

## 6. Urutan Prioritas Pengerjaan

### Prioritas 1 — Harus selesai terlebih dahulu

- [ ] Memastikan dataset dan periode penelitian.
- [ ] Memastikan seluruh file dan bulan yang tersedia.
- [ ] Membandingkan skema kolom.
- [ ] Membuat inventaris file.
- [ ] Menghasilkan laporan missing values, duplikat, dan rentang waktu.

### Prioritas 2 — Sebelum cleaning

- [ ] Menetapkan aturan missing values.
- [ ] Menetapkan aturan duplikat.
- [ ] Menetapkan kriteria outlier dan anomali.
- [ ] Menentukan cara menangani `PULocationID` dan `DOLocationID`.
- [ ] Membuat log perubahan dan penghapusan baris.

### Prioritas 3 — Sebelum pemodelan

- [ ] Menyelesaikan cleaning dan memvalidasi hasilnya.
- [ ] Menyusun feature dictionary.
- [ ] Menyelesaikan EDA.
- [ ] Menetapkan unit analisis dan target model.
- [ ] Mendokumentasikan metodologi final.

---

## 7. Kriteria Selesai Tahap Awal (_Definition of Done_)

Tahap awal dapat dianggap selesai apabila:

- [ ] Dataset dan periode penelitian telah diputuskan dengan alasan yang jelas.
- [ ] Semua file yang akan digunakan telah terinventarisasi.
- [ ] Struktur kolom dan tipe data telah diperiksa.
- [ ] Kualitas data telah diringkas dalam laporan.
- [ ] Aturan cleaning telah ditulis dan dapat diulang.
- [ ] Jumlah baris yang dihapus pada setiap tahap tercatat.
- [ ] Representasi lokasi telah ditentukan dan dijelaskan.
- [ ] Fitur yang akan dibuat telah didokumentasikan.
- [ ] EDA awal telah dilakukan dan temuan utamanya dicatat.
- [ ] Data mentah tetap tersimpan tanpa perubahan.

---

## 8. Catatan Keputusan yang Belum Final

- [ ] Dataset final: 2016 / 2026.
- [ ] Rentang bulan yang digunakan: **\*\*\*\***\_\_\_\_**\*\*\*\***.
- [ ] Tujuan utama penelitian: **\*\*\*\***\_\_\_\_**\*\*\*\***.
- [ ] Representasi lokasi: ID zona / centroid zona / koordinat GPS.
- [ ] Unit analisis: perjalanan / zona / zona × jam / lainnya.
- [ ] Model yang akan diuji: **\*\*\*\***\_\_\_\_**\*\*\*\***.
- [ ] Metrik evaluasi: **\*\*\*\***\_\_\_\_**\*\*\*\***.
- [ ] Alasan perubahan metodologi, jika ada: **\*\*\*\***\_\_\_\_**\*\*\*\***.

**Catatan:** jangan menganggap suatu aturan atau ambang cleaning sudah final sebelum memeriksa distribusi data dan menuliskan alasan pemilihannya.
