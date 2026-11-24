"""
Module src.data_processing
Menyediakan utilitas transformasi data, query lazy Polars, dan agregasi DuckDB.
"""

from pathlib import Path
from typing import Dict, Tuple
import duckdb
import polars as pl


def get_project_paths() -> Dict[str, Path]:
    """Mendapatkan path absolut struktur repositori proyek."""
    cwd = Path.cwd().resolve()
    if cwd.name == "notebooks":
        root = cwd.parent
    else:
        root = cwd
    
    return {
        "root": root,
        "raw_data": root / "data" / "raw" / "dataset.parquet",
        "processed_data": root / "data" / "processed" / "dataset_bersih.parquet",
        "figures": root / "output" / "figures",
    }


def assign_island_region(df_or_lazy: pl.LazyFrame) -> pl.LazyFrame:
    """
    Menambahkan kolom klasifikasi pulau/wilayah geografis utama Indonesia
    menggunakan ekspresi Polars berbasis rentang koordinat (lat, lon).
    """
    return df_or_lazy.with_columns(
        pl.when(
            (pl.col("lat") <= -5.0) & (pl.col("lat") >= -9.0) &
            (pl.col("lon") >= 105.0) & (pl.col("lon") <= 116.0)
        ).then(pl.lit("Jawa"))
        .when(
            (pl.col("lat") >= -6.0) & (pl.col("lat") <= 6.0) &
            (pl.col("lon") >= 95.0) & (pl.col("lon") <= 109.0)
        ).then(pl.lit("Sumatera"))
        .when(
            (pl.col("lat") >= -4.5) & (pl.col("lat") <= 4.5) &
            (pl.col("lon") >= 108.5) & (pl.col("lon") <= 119.5)
        ).then(pl.lit("Kalimantan"))
        .when(
            (pl.col("lat") >= -6.0) & (pl.col("lat") <= 2.5) &
            (pl.col("lon") >= 118.5) & (pl.col("lon") <= 125.5)
        ).then(pl.lit("Sulawesi"))
        .when(
            (pl.col("lat") <= -8.0) & (pl.col("lat") >= -11.5) &
            (pl.col("lon") >= 114.5) & (pl.col("lon") <= 126.0)
        ).then(pl.lit("Bali-Nusa Tenggara"))
        .when(
            (pl.col("lat") >= -9.0) & (pl.col("lat") <= 3.0) &
            (pl.col("lon") >= 125.0) & (pl.col("lon") <= 135.0)
        ).then(pl.lit("Maluku"))
        .when(
            (pl.col("lat") >= -10.0) & (pl.col("lat") <= 1.0) &
            (pl.col("lon") >= 130.0) & (pl.col("lon") <= 141.5)
        ).then(pl.lit("Papua"))
        .otherwise(pl.lit("Lainnya"))
        .alias("island")
    )


def clean_osm_pipeline(
    lazy_df: pl.LazyFrame,
    lat_bounds: Tuple[float, float] = (-11.5, 6.5),
    lon_bounds: Tuple[float, float] = (95.0, 141.5),
) -> pl.LazyFrame:
    """
    Pipeline pembersihan data LazyFrame Polars:
    1. Imputasi missing values: name -> 'Tanpa Nama', category -> 'unclassified'
    2. Winsorization / clipping koordinat geografis batas Indonesia
    3. Ekstraksi wilayah pulau (island)
    """
    return (
        lazy_df
        .with_columns([
            pl.col("name").fill_null("Tanpa Nama"),
            pl.col("category").fill_null("unclassified"),
            pl.col("lat").clip(lat_bounds[0], lat_bounds[1]),
            pl.col("lon").clip(lon_bounds[0], lon_bounds[1]),
        ])
        .pipe(assign_island_region)
    )


def get_duckdb_connection(parquet_path: Path) -> duckdb.DuckDBPyConnection:
    """Membuka koneksi DuckDB dan mendaftarkan view dataset."""
    con = duckdb.connect(database=":memory:")
    con.execute(f"CREATE VIEW IF NOT EXISTS dataset AS SELECT * FROM read_parquet('{parquet_path.as_posix()}')")
    return con
