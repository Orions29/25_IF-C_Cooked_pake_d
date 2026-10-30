import pandas as pd
import glob
import os
import numpy as np

# 1. Memuat seluruh data Parquet
folder_path = r"D:\3_Coding\2_Programming-Language\1-Python\sinauDatasains\projectAkhir_DS\data\parquet\2026"
file_pattern = os.path.join(folder_path, "yellow_tripdata_2026-*.parquet")
file_list = glob.glob(file_pattern)

print("Memuat berkas:")
for f in file_list:
    print(f"- {os.path.basename(f)}")

# Menggabungkan 6 bulan data menjadi satu DataFrame
df = pd.concat(
    [pd.read_parquet(f, engine="pyarrow") for f in file_list], ignore_index=True
)
print(f"\nTotal baris data: {len(df):,}")
print(f"Total kolom: {df.shape[1]}")

# 2. Pengecekan Missing Value
print("\n--- Pengecekan Missing Value ---")
missing_values = df.isnull().sum()
missing_cols = missing_values[missing_values > 0]
if missing_cols.empty:
    print("Tidak ada missing value pada seluruh kolom.")
else:
    print(missing_cols.to_frame(name="Jumlah Missing Value"))

# 3. Pengecekan Duplikasi
print("\n--- Pengecekan Duplikasi ---")
duplicate_count = df.duplicated().sum()
print(f"Jumlah baris duplikat: {duplicate_count:,}")

# 4. Pengecekan Outlier (menggunakan IQR pada kolom numerik penting)
print("\n--- Pengecekan Outlier (Metode IQR) ---")


def check_outliers_iqr(dataframe, column):
    # Mengabaikan NaN untuk kalkulasi
    series = dataframe[column].dropna()
    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outliers = series[(series < lower_bound) | (series > upper_bound)]
    skewness = series.skew()

    print(f"Kolom '{column}':")
    print(
        f"  - Jumlah Outlier : {len(outliers):,} ({(len(outliers)/len(series))*100:.2f}%)"
    )
    print(f"  - Skewness       : {skewness:.2f}")
    return outliers


_ = check_outliers_iqr(df, "trip_distance")
_ = check_outliers_iqr(df, "fare_amount")

# 5. Pengecekan Inkonsistensi (Domain Knowledge)
print("\n--- Pengecekan Inkonsistensi Logis ---")

# A. Tarif / Jarak Negatif
negative_fare = df[df["fare_amount"] < 0]
negative_distance = df[df["trip_distance"] < 0]
print(f"Tarif negatif (fare_amount < 0): {len(negative_fare):,} baris")
print(f"Jarak negatif (trip_distance < 0): {len(negative_distance):,} baris")

# B. Waktu Dropoff lebih awal dari Pickup (Mustahil secara fisik)
invalid_time = df[df["tpep_dropoff_datetime"] <= df["tpep_pickup_datetime"]]
print(f"Waktu dropoff <= pickup (Inkonsistensi waktu): {len(invalid_time):,} baris")

# C. Penumpang 0 (Nol)
zero_passenger = df[df["passenger_count"] == 0]
print(f"Jumlah penumpang 0: {len(zero_passenger):,} baris")

# D. Jarak 0 tetapi memiliki tarif dasar yang besar (misal > $5 selain tarif awal)
zero_dist_high_fare = df[(df["trip_distance"] == 0) & (df["fare_amount"] > 5.0)]
print(f"Jarak 0 mil tetapi tarif dasar > $5: {len(zero_dist_high_fare):,} baris")
