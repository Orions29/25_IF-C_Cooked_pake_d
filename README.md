# NYC Taxi Demand Analytics 🚕

**Analisis Spasial-Temporal dan Prediksi Taxi Demand di New York City**  
_Project Akhir Data Science_

## Tentang Proyek

Proyek ini menggunakan data **NYC Yellow Taxi** untuk mengeksplorasi pola permintaan taksi berdasarkan waktu dan lokasi, serta membangun model prediksi _taxi demand_.

Fokus analisis:

- **Temporal :** pola pickup berdasarkan jam, hari, dan bulan.
- **Spatial :** persebaran pickup berdasarkan Taxi Zone.
- **Forecasting :** pemodelan dan evaluasi prediksi permintaan.

## Struktur Folder

```text
projectAkhir_DS/
├── .vscode/                 # Konfigurasi VS Code
├── archive/                 # Arsip dan file sekali pakai
├── datasets/
│   ├── datasets_docs/       # Dokumentasi, peta, dan PDF dataset
│   ├── external/            # Data referensi eksternal
│   ├── interim/             # Data hasil cleaning dan transformasi
|   ├── processed            # Processed Dataset
│   ├── raw/                 # Data sumber asli
│   │   ├── 2016/
│   │   └── 2026/
│   │       └── withZone/    # Data 2026 yang telah dilengkapi informasi zona
│   └── zone/                # Shapefile dan lookup Taxi Zone
├── docs/                    # Catatan dan dokumentasi penelitian
├── out/
│   ├── html/                 # Peta interaktif
│   └── output_eda/           # Grafik dan tabel hasil EDA
├── script/
│   ├── scratch/              # Eksperimen sementara
│   └── tools/                # Notebook dan utilitas pendukung
├── .gitignore
└── README.md
```

**Aturan penyimpanan:** simpan data sumber tanpa perubahan di `datasets/raw/`, hasil cleaning atau transformasi di `datasets/interim/`, dan hasil analisis di `out/`. Folder `withZone/` berisi data hasil join, sehingga untuk konsistensi sebaiknya dipindahkan ke `datasets/interim/2026/`.

Folder `datasets/processed/` digunakan untuk menyimpan dataset
hasil pengolahan yang siap digunakan dalam analisis dan pemodelan.

## Persiapan Dataset

Unduh dataset melalui [Google Drive - Dataset Proyek](https://drive.google.com/drive/folders/1icM9a2faBhOn-KZ-frdPWTNHdGcPMHO3?usp=sharing), kemudian:

1. Ekstrak file ZIP yang diperlukan.
2. Peletakan Hasil Extract:
   2.a) Letakkan data Yellow Taxi 2026 di `datasets/raw`.
   2.b) Jika Memakai `datasets.zip` maka tinggal paste di root menggantikan folder `datasets`.
3. Pastikan file sudah berada di folder yang sesuai sebelum menjalankan notebook.

> Data mentah sebaiknya tidak diedit atau ditimpa!! Simpan seluruh hasil pemrosesan sebagai file baru.

## Setup Environment

Proyek ini menggunakan Python 3.13 dan virtual environment untuk menjaga konsistensi dependensi.

### 1. Membuat Virtual Environment

Jalankan perintah berikut melalui Windows PowerShell:

```powershell
# Buat virtual environment menggunakan Python 3.13
py -3.13 -m venv .venv

# Aktifkan virtual environment
.\.venv\Scripts\Activate.ps1
```

### 2. Menginstal Dependencies

Pastikan virtual environment sudah aktif, kemudian jalankan:

```powershell
# Perbarui pip
python -m pip install --upgrade pip

# Instal seluruh dependencies proyek
python -m pip install -r requirements.txt
```

### 3. Memeriksa Dependencies

Untuk memastikan seluruh dependencies terpasang dengan benar:

```powershell
python -m pip check
```

### 4. Konfigurasi VS Code

1. Buka Command Palette dengan `Ctrl + Shift + P`.
2. Pilih `Python: Select Interpreter`.
3. Pilih interpreter dari folder `.venv`.
4. Jika menggunakan Jupyter Notebook, pilih kernel dari environment yang sama.



### Catatan

Daftar library dan versi yang digunakan dalam proyek disimpan di `requirements.txt`.

Gunakan file tersebut sebagai acuan instalasi dependencies agar environment antaranggota kelompok lebih konsisten.


## Menjalankan Proyek

Jalankan notebook di dalam folder `script/` mengikuti nomor dan urutan analisis yang tersedia. Alur umumnya:

1. **Data preparation** - pemeriksaan data, cleaning, dan preprocessing.
2. **EDA** - eksplorasi pola temporal dan spasial.
3. **Feature engineering** - agregasi demand dan pembuatan fitur model.
4. **Modeling** - training, prediksi, dan evaluasi.

Simpan hasil visualisasi, tabel, dan peta pada folder `out/` agar terpisah dari notebook dan data sumber.

## Reproducibility & Catatan Penelitian

- Catat periode data, sumber, dan proses preprocessing yang digunakan.
- Gunakan definisi _taxi demand_ yang konsisten; contoh: jumlah pickup per zona per jam.
- Tetapkan `random_state`/seed dan parameter eksperimen ketika menggunakan proses acak.
- Pisahkan data training dan testing berdasarkan waktu untuk menghindari _data leakage_.
- Dokumentasikan fitur, model, metrik evaluasi, serta keterbatasan hasil.
- Periksa kesesuaian skema kolom sebelum membandingkan data 2016 dan 2026. Kedua periode tersebut tidak membentuk deret waktu kontinu.

## Referensi

- [NYC TLC - Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)
- [NYC TLC - Data Dictionary](https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf)
- [NYC TLC - Trip Record User Guide](https://www.nyc.gov/assets/tlc/downloads/pdf/trip_record_user_guide.pdf)
