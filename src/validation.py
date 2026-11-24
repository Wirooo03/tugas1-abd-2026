"""
Module src.validation
Menyediakan aturan validasi integritas kualitas data (Data Quality Rules)
berdasarkan 6 dimensi kualitas data di skala besar.
"""

from typing import Dict, Any
import duckdb
import polars as pl


def validate_osm_data_quality(con: duckdb.DuckDBPyConnection, view_name: str = "dataset") -> Dict[str, Any]:
    """
    Menjalankan audit kualitas data menyeluruh menggunakan DuckDB SQL.
    Mengukur dimensi: Completeness, Spatial Validity, Uniqueness, dan Consistency.
    """
    query = f"""
    SELECT
        COUNT(*) AS total_baris,
        COUNT(DISTINCT osm_id) AS osm_id_unik,
        SUM(CASE WHEN name IS NULL OR category IS NULL OR lat IS NULL OR lon IS NULL THEN 1 ELSE 0 END) AS null_violations,
        SUM(CASE WHEN lat < -11.5 OR lat > 6.5 OR lon < 95.0 OR lon > 141.5 THEN 1 ELSE 0 END) AS spatial_boundary_violations,
        SUM(CASE WHEN osm_type NOT IN ('node', 'way', 'relation') THEN 1 ELSE 0 END) AS invalid_osm_types,
        MIN(lat) AS min_lat,
        MAX(lat) AS max_lat,
        MIN(lon) AS min_lon,
        MAX(lon) AS max_lon
    FROM {view_name}
    """
    res = con.execute(query).fetchdf()
    row = res.iloc[0]
    
    total_baris = int(row["total_baris"])
    unique_ids = int(row["osm_id_unik"])
    null_violations = int(row["null_violations"])
    boundary_violations = int(row["spatial_boundary_violations"])
    invalid_types = int(row["invalid_osm_types"])
    
    completeness_score = ((total_baris - null_violations) / total_baris) * 100 if total_baris > 0 else 0
    spatial_validity_score = ((total_baris - boundary_violations) / total_baris) * 100 if total_baris > 0 else 0
    uniqueness_score = (unique_ids / total_baris) * 100 if total_baris > 0 else 0
    
    is_valid = (
        null_violations == 0 and
        boundary_violations == 0 and
        invalid_types == 0 and
        total_baris >= 1_000_000
    )
    
    return {
        "is_valid": is_valid,
        "total_baris": total_baris,
        "unique_ids": unique_ids,
        "duplicates": total_baris - unique_ids,
        "null_violations": null_violations,
        "boundary_violations": boundary_violations,
        "invalid_types": invalid_types,
        "completeness_score": completeness_score,
        "spatial_validity_score": spatial_validity_score,
        "uniqueness_score": uniqueness_score,
        "bounds": {
            "lat": (float(row["min_lat"]), float(row["max_lat"])),
            "lon": (float(row["min_lon"]), float(row["max_lon"])),
        }
    }
