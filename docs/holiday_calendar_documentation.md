
# Dokumentasi Kalender Hari Libur dan Event NYC 2026

## 1. Gambaran Umum

Kalender ini berisi informasi mengenai hari libur nasional Amerika Serikat (*Federal Holidays*) dan berbagai event khusus di New York City (NYC) selama periode Januari hingga Juni 2026.

Kalender dibuat untuk mendukung proses rekayasa fitur (*feature engineering*) pada proyek prediksi permintaan taksi NYC Yellow Taxi.

## 2. Sumber Data

Sumber data yang digunakan:

- `datasets/datasets_docs/FederalHolidays_Event.md`

File sumber berisi 19 entri hari libur dan event, yang terdiri dari tanggal tunggal maupun rentang tanggal.

## 3. Proses Pengolahan Data

Kalender dibuat menggunakan Python dengan bantuan library Pandas.

Tahapan pengolahan data:

1. Mendefinisikan nama event, tanggal mulai, tanggal selesai, dan kategori setiap event.
2. Membuat rentang tanggal harian dari 1 Januari hingga 30 Juni 2026.
3. Mengidentifikasi event yang berlangsung pada setiap tanggal.
4. Menggabungkan beberapa event apabila berlangsung pada tanggal yang sama.
5. Membuat fitur indikator biner berdasarkan kategori event.
6. Menyimpan hasil pengolahan ke dalam file CSV.

## 4. Hasil Pengolahan

Lokasi file hasil:

- `datasets/processed/nyc_holiday_event_calendar_2026.csv`

Dimensi dataset:

- Jumlah baris: 181
- Jumlah kolom: 11
- Rentang tanggal: 2026-01-01 sampai 2026-06-30

## 5. Deskripsi Fitur

| Nama Fitur | Deskripsi |
|---|---|
| `date` | Tanggal kalender |
| `event_names` | Nama event yang berlangsung pada tanggal tersebut |
| `categories` | Kategori seluruh event yang berlangsung |
| `is_holiday` | Indikator hari libur nasional AS |
| `is_event` | Indikator adanya event atau observansi non-federal |
| `is_major_nyc_event` | Indikator event besar di NYC |
| `is_cultural_observance` | Indikator observansi budaya |
| `is_religious_observance` | Indikator observansi keagamaan |
| `is_general_observance` | Indikator observansi umum |
| `is_event_observance` | Indikator kategori event/observance |
| `event_categories` | Kategori event non-federal yang berlangsung |

Nilai indikator biner:
- `1` menunjukkan kondisi atau event tersebut berlangsung.
- `0` menunjukkan kondisi atau event tersebut tidak berlangsung.

## 6. Validasi Data

Validasi dilakukan untuk memastikan hasil pengolahan sesuai dengan rentang tanggal dan data sumber.

Hasil validasi:

- Jumlah data harian: 181 baris.
- Jumlah tanggal Federal Holiday: 5 hari.
- Jumlah tanggal dengan event non-federal: 123 hari.
- Jumlah tanggal duplikat: 0.
- Seluruh tanggal dalam periode Januari–Juni 2026 berhasil dibuat.

## 7. Pemanfaatan untuk Machine Learning

Kalender ini digunakan sebagai sumber fitur tambahan untuk model prediksi permintaan taksi.

Fitur indikator biner dapat digabungkan dengan dataset permintaan taksi per jam (*hourly taxi demand dataset*) menggunakan kolom `date`.

Fitur kalender diharapkan dapat membantu model mengenali karakteristik tanggal, seperti hari libur nasional, event besar, dan observansi tertentu.

Sebelum digunakan dalam pelatihan model SVM, data kalender perlu diselaraskan dengan struktur tanggal dan waktu pada dataset taksi.
