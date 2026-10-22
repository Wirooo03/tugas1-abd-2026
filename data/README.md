# Data Tugas 1

## Dataset yang Dipilih

Isi informasi berikut sebelum Milestone 1.

| Item | Isi |
|---|---|
| Nama dataset | Indonesia POI: OpenStreetMap Detail |
| Sumber | [Hugging Face: Lyon28/indonesia-poi-openStreetMaps](https://huggingface.co/datasets/Lyon28/indonesia-poi-openStreetMaps) (ekstrak dari Geofabrik OpenStreetMap Indonesia) |
| Lisensi/ketentuan pakai | Open Database License (ODbL) v1.0 |
| Ukuran | 846,4 MB (Parquet terkompresi) / 51.842.020 baris |
| Periode data | 2024 (snapshot pembaruan OpenStreetMap Indonesia) |
| Unit analisis | Entitas objek spasial & Point of Interest (node, way, relation) di wilayah Indonesia |

## Deskripsi Kolom Dataset

Dataset tersimpan dalam format Apache Parquet dengan skema sebagai berikut:

| Nama Kolom | Tipe Data | Keterangan |
|---|---|---|
| `osm_type` | `string` | Tipe geometri/objek OSM (`node`, `way`, atau `relation`). |
| `osm_id` | `int64` | Identifier unik objek di OpenStreetMap. |
| `name` | `string` | Nama fasilitas/tempat (bisa null jika objek tidak bernama khusus). |
| `category` | `string` | Kategori fasilitas utama (contoh: `amenity=school`, `amenity=cafe`, `shop=convenience`). |
| `lat` | `float64` | Koordinat lintang (latitude) sistem WGS84. |
| `lon` | `float64` | Koordinat bujur (longitude) sistem WGS84. |
| `tags_json` | `string` | Seluruh atribut dan metadata tag OSM dalam format serialized JSON. |

## Tempat Mencari Dataset

Pilih dataset Indonesia yang legal digunakan, dapat didokumentasikan sumbernya, dan memenuhi batas ukuran tugas.

| Situs | Kegunaan |
|---|---|
| [Satu Data Indonesia](https://data.go.id/) | Portal data terbuka lintas instansi pemerintah Indonesia. |
| [Badan Pusat Statistik](https://www.bps.go.id/) | Statistik sosial, ekonomi, kependudukan, dan data wilayah. |
| [BMKG Data Online](https://dataonline.bmkg.go.id/) | Data cuaca, iklim, gempa bumi, dan observasi meteorologi. |
| [Hugging Face Datasets](https://huggingface.co/datasets) | Dataset publik yang dapat dicari berdasarkan topik, bahasa, atau ukuran. |
| [Kaggle Datasets](https://www.kaggle.com/datasets) | Katalog dataset publik; periksa lisensi dan dokumentasi pembuatnya. |
| [Google Dataset Search](https://datasetsearch.research.google.com/) | Mesin pencari untuk menemukan dataset dari berbagai portal. |

## Cara Memperoleh Data

1. Unduh file `openstreetmap.parquet` dari Hugging Face ke folder `data/raw/dataset.parquet` menggunakan salah satu cara berikut:

   **Menggunakan Python / curl:**
   ```bash
   curl -L "https://huggingface.co/datasets/Lyon28/indonesia-poi-openStreetMaps/resolve/main/parquet/openstreetmap.parquet" -o "data/raw/dataset.parquet"
   ```

   **Atau menggunakan script Python:**
   ```python
   import urllib.request
   from pathlib import Path

   url = "https://huggingface.co/datasets/Lyon28/indonesia-poi-openStreetMaps/resolve/main/parquet/openstreetmap.parquet"
   dest = Path("data/raw/dataset.parquet")
   dest.parent.mkdir(parents=True, exist_ok=True)
   urllib.request.urlretrieve(url, dest)
   ```

2. Pastikan file berukuran sekitar 846,4 MB (846.399.350 bytes).
3. Pastikan variabel `DATA_PATH` pada `notebooks/01_data_profiling.ipynb` mengarah ke:
   ```python
   DATA_PATH = PROJECT_ROOT / 'data' / 'raw' / 'dataset.parquet'
   ```

## Aturan Penyimpanan

- Jangan commit dataset mentah atau hasil olahan berukuran besar ke Git (folder `data/raw/*` dan `data/processed/*` sudah diatur dalam `.gitignore`).
- File pada `data/raw/` adalah data asli dan tidak boleh diubah secara destruktif.
- Simpan hasil transformasi data bersih yang dapat direproduksi pada `data/processed/`.
