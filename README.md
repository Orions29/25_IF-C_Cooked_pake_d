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

## Persiapan Dataset

Unduh dataset melalui [Google Drive - Dataset Proyek](https://drive.google.com/drive/folders/1WIKaykwoGqCRWO_QsLUs9Zu), kemudian:

1. Ekstrak file ZIP yang diperlukan.
2. Letakkan data Yellow Taxi 2026 di `datasets/raw/`.
3. Pastikan file sudah berada di folder yang sesuai sebelum menjalankan notebook.

> Data mentah sebaiknya tidak diedit atau ditimpa!! Simpan seluruh hasil pemrosesan sebagai file baru.

## Setup Environment

Contoh setup menggunakan Windows PowerShell:

```powershell
# Buat virtual environment
py -m venv .venv

# Aktifkan environment
.\.venv\Scripts\Activate.ps1

# Install library yang dibutuhkan
python -m pip install --upgrade pip
python -m pip install pandas numpy matplotlib seaborn pyarrow jupyter
```

Sesuaikan library tambahan dengan notebook yang digunakan, lalu pilih `.venv` sebagai Python interpreter/kernel di VS Code.

Library Yang Digunakan:

1. Python 3.14.7
2. pandas 3.0.6
3. numpy 2.5.3
4. scipy 1.18.1
5. seaborn 0.13.2

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
