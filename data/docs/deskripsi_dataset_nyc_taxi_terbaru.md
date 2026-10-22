# Kamus Data - Catatan Perjalanan Taksi Kuning NYC (NYC Yellow Taxi)
*Pembaruan Resmi: Maret 2025*

Dokumen ini berisi penjelasan resmi mengenai atribut/kolom pada dataset perjalanan Taksi Kuning (*Yellow Taxi*) New York City (NYC) Taxi & Limousine Commission (TLC).

---

## Tabel Atribut Data

| Nama Kolom (*Field Name*) | Tipe Data | Deskripsi |
| :--- | :--- | :--- |
| `VendorID` | `int32` | Kode penyedia teknologi TPEP yang mencatat perjalanan:<br>• **1** = Creative Mobile Technologies, LLC<br>• **2** = Curb Mobility, LLC<br>• **6** = Myle Technologies Inc<br>• **7** = Helix |
| `tpep_pickup_datetime` | `datetime64[us]` | Tanggal dan waktu saat argometer (*taximeter*) diaktifkan/dinyalakan. |
| `tpep_dropoff_datetime` | `datetime64[us]` | Tanggal dan waktu saat argometer dimatikan. |
| `passenger_count` | `float64` | Jumlah penumpang di dalam kendaraan (nilai diinput oleh pengemudi). |
| `trip_distance` | `float64` | Jarak perjalanan yang ditempuh dalam satuan mil (*miles*) sesuai laporan argometer. |
| `RatecodeID` | `float64` | Kode tarif akhir yang berlaku pada akhir perjalanan:<br>• **1** = Standard rate<br>• **2** = JFK<br>• **3** = Newark<br>• **4** = Nassau / Westchester<br>• **5** = Negotiated fare<br>• **6** = Group ride<br>• **99** = Null / Unknown |
| `store_and_fwd_flag` | `str` | Menandakan apakah catatan perjalanan disimpan di memori kendaraan sebelum dikirim ke vendor karena masalah koneksi (*store and forward*):<br>• **Y** = *Store and forward trip*<br>• **N** = *Not a store and forward trip* |
| `PULocationID` | `int32` | Kode Wilayah Zona Taksi TLC (*TLC Taxi Zone*) tempat argometer diaktifkan (lokasi penjemputan/pickup). |
| `DOLocationID` | `int32` | Kode Wilayah Zona Taksi TLC (*TLC Taxi Zone*) tempat argometer dimatikan (lokasi penurunan/dropoff). |
| `payment_type` | `int64` | Kode numerik metode pembayaran yang digunakan penumpang:<br>• **0** = Flex Fare trip<br>• **1** = Credit card<br>• **2** = Cash<br>• **3** = No charge<br>• **4** = Dispute<br>• **5** = Unknown<br>• **6** = Voided trip |
| `fare_amount` | `float64` | Tarif dasar perjalanan berdasarkan waktu dan jarak yang dihitung oleh argometer. |
| `extra` | `float64` | Biaya tambahan bervariasi dan *surcharge* (seperti biaya jam sibuk $0.50 atau biaya malam hari $1.00). |
| `mta_tax` | `float64` | Pajak MTA sebesar $0.50 yang terpicu otomatis berdasarkan jenis tarif yang digunakan. |
| `tip_amount` | `float64` | Jumlah tip. Field ini terisi otomatis **hanya** untuk tip transaksi kartu kredit. Tip tunai tidak tercatat dalam sistem. |
| `tolls_amount` | `float64` | Total biaya tol yang dibayar selama perjalanan. |
| `improvement_surcharge` | `float64` | Biaya tambahan pembenahan (*improvement surcharge*) sebesar $0.30 yang dikenakan saat argometer dinyalakan (berlaku sejak 2015). |
| `total_amount` | `float64` | Total biaya keseluruhan yang ditagihkan kepada penumpang (tidak termasuk tip tunai). |
| `congestion_surcharge` | `float64` | Total biaya tambahan kemacetan (*NYS Congestion Surcharge*) yang dikumpulkan dalam perjalanan. |
| `Airport_fee` | `float64` | Biaya tambahan bandara khusus penjemputan di Bandara LaGuardia (LGA) dan John F. Kennedy (JFK). |
| `cbd_congestion_fee` | `float64` | Biaya per perjalanan untuk skema *MTA Congestion Relief Zone* (Central Business District) yang berlaku mulai 5 Januari 2025. |

---

## Catatan Penting Mengenai Dataset Terbaru:
1. **PULocationID & DOLocationID**: Dataset versi ini tidak lagi menyediakan titik GPS (`latitude`/`longitude`). Untuk mengetahui nama wilayah/borough (misal: *Manhattan*, *JFK Airport*), kamu perlu menghubungkan ID ini dengan file **Taxi Zone Lookup Table** resmi dari TLC.
2. **Biaya Tambahan Baru**: Terdapat kolom biaya baru seperti `congestion_surcharge`, `Airport_fee`, dan `cbd_congestion_fee` yang disesuaikan dengan regulasi lalu lintas terkini di NYC (termasuk aturan 2025).