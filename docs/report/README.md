# Index Laporan

Peta artefak per fase. ✅ = laporan naratif sudah ada; ❌ = notebook & output ada, tapi laporan naratif belum dibuat.

| Fase | Notebook | Output utama | Laporan |
|:--|:--|:--|:--|
| 1 Audit | `0_data_audit`, `00_audit_outputs` | `out/output_eda/00_*`, `01_*`, `02_*` | ✅ `1_audit_dataset/laporan_audit.md` |
| 2A Cleaning | `1_data_cleaning` | `main_trips.parquet`, `03_cleaning_log.csv` | ✅ `2a_cleaning/laporan_cleaning.md` |
| 2B Zona & join koordinat | bagian dari `1_data_cleaning` | `zone_centroid_lookup.csv` | ✅ (termasuk di laporan cleaning) |
| 3 EDA | `2_EDA_Yellow_taxi` | grafik & tabel EDA | ❌ belum ada |
| 4A Agregasi | `04a_aggregation` | `demand_zone_hour.parquet` | ❌ belum ada |
| 4B Spasial | `04b_spatial_analysis` | `out/output_eda/04b_*`, peta HTML | ❌ belum ada |
| 5 Feature engineering | `05_features` | `features_dataset`, `timeseries_*` | ✅ `2b_feature_engineering/laporan_feature_engineering.md` |
| 6A Baseline | `06_baseline` | `out/output_eda/06_baseline_*` | ✅ `3_baseline/laporan_baseline.md` |
| 6B Regresi | `06_regression`, `07_tuning_regression` | `out/regression/*` | ❌ belum ada |
| 6C SVM | `07_svm_classification_ready`, `08_svm_optimization & experiments`, `10_svm_final_testing` | `out/svm/*`, `out/svm_final_*` | ❌ belum ada |
| 6D Time series | `08_time_series` | `out/output_eda/08_ts_*` | ❌ belum ada |
| 7 Optimasi & trade-off | `09_optimization_tradeoff` | trade-off & coverage@K (belum lengkap) | ❌ belum ada |

## Perlu dirapatkan

Daftar lengkap ada di `docs/analysis_plan.md` bagian 15. Ringkasnya:

- Sumber final `demand_zone_hour`: `04a_aggregation` atau `05_features` (keduanya menulis file yang sama).
- Tabel trade-off dan grafik coverage@K belum tersimpan.
- Peta hotspot HTML `04b_hotspot_all.html` belum ada di `out/html/`.
- Model final (dari validation) belum diumumkan; evaluasi test hanya sekali.
