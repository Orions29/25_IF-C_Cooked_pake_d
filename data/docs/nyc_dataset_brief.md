# Tentang Dataset

## Konteks

_New York City (NYC) Taxi & Limousine Commission_ (TLC) menyimpan data dari seluruh armada taksinya. Data ini tersedia secara gratis untuk diunduh melalui situs web resminya. Secara umum, TLC mengelola data untuk 4 jenis kendaraan utama:

- **Taksi Kuning (_Yellow Taxi_)**: _Yellow Medallion Taxicabs_ — Taksi kuning ikonik NYC yang menyediakan layanan transportasi khusus melalui cegatan langsung di jalan (_street hails_). Jumlah armada dibatasi oleh jumlah izin (_medallion_) resmi yang dikeluarkan oleh TLC.
- **Taksi Hijau (_Green Taxi_)**: _Street Hail Livery (SHL)_ — Program SHL mengizinkan pemilik kendaraan _livery_ untuk mendaftarkan dan melengkapi kendaraan mereka dengan identitas taksi hijau, argometer, mesin kartu kredit, serta hak untuk menerima cegatan di jalan selain pesanan berbasis pra-pemesanan (_pre-arranged rides_).
- **Kendaraan Sewa (_For-Hire Vehicles / FHVs_)**: Layanan transportasi yang diakses melalui pemesanan terlebih dahulu (_pre-arrangement_) lewat _dispatcher_ atau perusahaan limosin. FHV tidak diizinkan mengambil penumpang dari cegatan langsung di jalan.

## Kernel Pelengkap

- Tersedia Kernel khusus untuk dataset ini yang menerapkan teknik analisis _Clustering_, _Regression_, dan _Time-Series_.

## Poin-Poin Penting

- Dataset ini khusus mencakup **Data Taksi Kuning** untuk periode **Januari-Maret 2016** dan **Januari–Juni 2026**.
- Jika Anda mengunduh file CSV langsung dari situs web NYC TLC saat ini, Anda akan menemukan format yang berbeda karena TLC secara berkala memperbarui data mereka.
- Perubahan utama pada format baru TLC adalah penggunaan indeks wilayah/zona alih-alih koordinat geografis (_latitude_ & _longitude_).
- Dataset ini sengaja menggunakan versi file CSV sebelumnya agar memungkinkan praktik analisis _clustering_ berbasis titik lokasi koordinat presisi serta analisis _time-series_.

---

## Tabel Atribut Data

| Nama Kolom (_Field Name_) | Tipe Data        | Deskripsi                                                                                                                                                                                                                                |
| :------------------------ | :--------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `VendorID`                | `int32`          | Kode penyedia teknologi TPEP yang mencatat perjalanan:<br>• **1** = Creative Mobile Technologies, LLC<br>• **2** = Curb Mobility, LLC<br>• **6** = Myle Technologies Inc<br>• **7** = Helix                                              |
| `tpep_pickup_datetime`    | `datetime64[us]` | Tanggal dan waktu saat argometer (_taximeter_) diaktifkan/dinyalakan.                                                                                                                                                                    |
| `tpep_dropoff_datetime`   | `datetime64[us]` | Tanggal dan waktu saat argometer dimatikan.                                                                                                                                                                                              |
| `passenger_count`         | `float64`        | Jumlah penumpang di dalam kendaraan (nilai diinput oleh pengemudi).                                                                                                                                                                      |
| `trip_distance`           | `float64`        | Jarak perjalanan yang ditempuh dalam satuan mil (_miles_) sesuai laporan argometer.                                                                                                                                                      |
| `RatecodeID`              | `float64`        | Kode tarif akhir yang berlaku pada akhir perjalanan:<br>• **1** = Standard rate<br>• **2** = JFK<br>• **3** = Newark<br>• **4** = Nassau / Westchester<br>• **5** = Negotiated fare<br>• **6** = Group ride<br>• **99** = Null / Unknown |
| `store_and_fwd_flag`      | `str`            | Menandakan apakah catatan perjalanan disimpan di memori kendaraan sebelum dikirim ke vendor karena masalah koneksi (_store and forward_):<br>• **Y** = _Store and forward trip_<br>• **N** = _Not a store and forward trip_              |
| `PULocationID`            | `int32`          | Kode Wilayah Zona Taksi TLC (_TLC Taxi Zone_) tempat argometer diaktifkan (lokasi penjemputan/pickup).                                                                                                                                   |
| `DOLocationID`            | `int32`          | Kode Wilayah Zona Taksi TLC (_TLC Taxi Zone_) tempat argometer dimatikan (lokasi penurunan/dropoff).                                                                                                                                     |
| `payment_type`            | `int64`          | Kode numerik metode pembayaran yang digunakan penumpang:<br>• **0** = Flex Fare trip<br>• **1** = Credit card<br>• **2** = Cash<br>• **3** = No charge<br>• **4** = Dispute<br>• **5** = Unknown<br>• **6** = Voided trip                |
| `fare_amount`             | `float64`        | Tarif dasar perjalanan berdasarkan waktu dan jarak yang dihitung oleh argometer.                                                                                                                                                         |
| `extra`                   | `float64`        | Biaya tambahan bervariasi dan _surcharge_ (seperti biaya jam sibuk $0.50 atau biaya malam hari $1.00).                                                                                                                                   |
| `mta_tax`                 | `float64`        | Pajak MTA sebesar $0.50 yang terpicu otomatis berdasarkan jenis tarif yang digunakan.                                                                                                                                                    |
| `tip_amount`              | `float64`        | Jumlah tip. Field ini terisi otomatis **hanya** untuk tip transaksi kartu kredit. Tip tunai tidak tercatat dalam sistem.                                                                                                                 |
| `tolls_amount`            | `float64`        | Total biaya tol yang dibayar selama perjalanan.                                                                                                                                                                                          |
| `improvement_surcharge`   | `float64`        | Biaya tambahan pembenahan (_improvement surcharge_) sebesar $0.30 yang dikenakan saat argometer dinyalakan (berlaku sejak 2015).                                                                                                         |
| `total_amount`            | `float64`        | Total biaya keseluruhan yang ditagihkan kepada penumpang (tidak termasuk tip tunai).                                                                                                                                                     |
| `congestion_surcharge`    | `float64`        | Total biaya tambahan kemacetan (_NYS Congestion Surcharge_) yang dikumpulkan dalam perjalanan.                                                                                                                                           |
| `Airport_fee`             | `float64`        | Biaya tambahan bandara khusus penjemputan di Bandara LaGuardia (LGA) dan John F. Kennedy (JFK).                                                                                                                                          |
| `cbd_congestion_fee`      | `float64`        | Biaya per perjalanan untuk skema _MTA Congestion Relief Zone_ (Central Business District) yang berlaku mulai 5 Januari 2025.                                                                                                             |

---

## Catatan Penting Mengenai Dataset Terbaru:

1. **PULocationID & DOLocationID**: Dataset versi ini tidak lagi menyediakan titik GPS (`latitude`/`longitude`). Untuk mengetahui nama wilayah/borough (misal: _Manhattan_, _JFK Airport_), kamu perlu menghubungkan ID ini dengan file **Taxi Zone Lookup Table** resmi dari TLC.
2. **Biaya Tambahan Baru**: Terdapat kolom biaya baru seperti `congestion_surcharge`, `Airport_fee`, dan `cbd_congestion_fee` yang disesuaikan dengan regulasi lalu lintas terkini di NYC (termasuk aturan 2025).

## Pengakuan (_Acknowledgements_)

- _New York City's Taxi & Limousine Commission_ (TLC)
