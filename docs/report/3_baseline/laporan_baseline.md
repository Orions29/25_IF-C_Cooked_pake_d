# Laporan Baseline (Fase 6A)

Baseline wajib sebagai pembanding semua model di Fase 6. Dijalankan dari `script/06_baseline.ipynb`, metrik dari `script/tools/metrics.py`.

- Regresi / time series: **Seasonal Naive** = `lag_168` (pickup jam yang sama minggu lalu).
- Klasifikasi: **kelas mayoritas** dan **kelas dari `lag_168`**.
- Data: `features_dataset.parquet`. Validation = Mei, Test = Juni.
- MASE memakai pembagi dari training: rata-rata |aktual − `lag_168`| = **5,079**.

## 1. Baseline Regresi (Seasonal Naive)

| Periode | MAE | RMSE | WAPE | R² | MASE |
|:--|--:|--:|--:|--:|--:|
| Validation (Mei) | 5,2773 | 16,0275 | 0,2582 | 0,9206 | 1,0390 |
| Test (Juni) | 4,8875 | 15,4584 | 0,2470 | 0,9216 | 0,9622 |

MASE < 1 di test artinya seasonal naive sedikit lebih baik dari rata-rata error training-nya sendiri.

## 2. Baseline Klasifikasi

| Periode | Model | Accuracy | Precision (macro) | Recall (macro) | F1 (macro) |
|:--|:--|--:|--:|--:|--:|
| Validation | mayoritas | 0,3917 | 0,1306 | 0,3333 | 0,1876 |
| Validation | lag_168 | 0,7408 | 0,7363 | 0,7363 | 0,7363 |
| Test | mayoritas | 0,4923 | 0,1641 | 0,3333 | 0,2199 |
| Test | lag_168 | 0,7522 | 0,7263 | 0,7331 | 0,7292 |

Confusion matrix `lag_168` di test (baris = aktual):

| aktual \ pred | Rendah | Sedang | Tinggi |
|:--|--:|--:|--:|
| Rendah | 72.382 | 19.918 | 917 |
| Sedang | 15.432 | 22.658 | 5.706 |
| Tinggi | 449 | 4.502 | 47.396 |

## 3. Catatan

- Baseline `lag_168` sudah cukup kuat; model di 6B/6C/6D harus mengalahkan angka ini untuk dinyatakan layak.
- Baseline klasifikasi kelas mayoritas jelek (macro-F1 ~0,19–0,22), jadi macro-F1 `lag_168` (~0,73) yang dipakai sebagai target minimal.
- Prediksi baseline disimpan di `out/output_eda/06_baseline_predictions_{validation,test}.parquet` dan metrik di `out/output_eda/06_baseline_*.csv` (folder output tidak ikut git).
