"""
Module src.visualization
Menyediakan fungsi pembangun visualisasi interaktif Plotly
serta utilitas ekspor grafik mandiri (HTML).
"""

from pathlib import Path
from typing import Dict
import plotly.express as px
import plotly.graph_objects as go
import polars as pl


THEME_COLORS = {
    "primary": "#1f77b4",
    "secondary": "#ff7f0e",
    "accent": "#2ca02c",
    "background": "#ffffff",
    "grid": "#eaeaea",
    "palette": ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]
}


def plot_spatial_density_map(sample_df: pl.DataFrame) -> go.Figure:
    """
    Visualisasi 1: Peta Sebaran Spasial POI di Seluruh Indonesia.
    Menggunakan Plotly scatter geo / coordinate density map.
    """
    df_p = sample_df.to_pandas()
    fig = px.scatter(
        df_p,
        x="lon",
        y="lat",
        color="island",
        hover_data=["name", "category", "osm_type"],
        title="<b>Peta Interaktif Sebaran POI dan Fasilitas Spasial Indonesia</b><br><sup>Menunjukkan konsentrasi tinggi di koridor Pulau Jawa dan kota-kota pelabuhan utama</sup>",
        labels={"lon": "Bujur (Longitude °E)", "lat": "Lintang (Latitude °S/°N)", "island": "Wilayah Pulau"},
        opacity=0.6,
        color_discrete_sequence=THEME_COLORS["palette"],
        template="plotly_white"
    )
    fig.update_layout(
        height=550,
        xaxis=dict(range=[94.0, 142.0], gridcolor=THEME_COLORS["grid"]),
        yaxis=dict(range=[-12.0, 7.0], gridcolor=THEME_COLORS["grid"]),
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5)
    )
    return fig


def plot_island_disparity_bar(island_df: pl.DataFrame) -> go.Figure:
    """
    Visualisasi 2: Disparitas Kepadatan POI Antar Wilayah Pulau (Jawa vs Luar Jawa).
    """
    df_p = island_df.sort("jumlah_poi", descending=True).to_pandas()
    fig = px.bar(
        df_p,
        x="island",
        y="jumlah_poi",
        color="persentase",
        text="persentase",
        title="<b>Disparitas Kepadatan Infrastruktur: Jawa-Sentris vs Wilayah Luar Jawa</b><br><sup>Proporsi total fasilitas dan infrastruktur geospasial OpenStreetMap per kepulauan</sup>",
        labels={"island": "Wilayah Pulau", "jumlah_poi": "Total POI / Fasilitas", "persentase": "Proporsi (%)"},
        color_continuous_scale="Tealgrn",
        template="plotly_white"
    )
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig.update_layout(
        height=500,
        yaxis=dict(title="Jumlah Fasilitas Terdata", gridcolor=THEME_COLORS["grid"]),
        coloraxis_colorbar=dict(title="% Total")
    )
    return fig


def plot_top_categories_bar(cat_df: pl.DataFrame) -> go.Figure:
    """
    Visualisasi 3: Top 15 Kategori Fasilitas Terbanyak di Indonesia.
    """
    df_p = cat_df.head(15).sort("jumlah", descending=False).to_pandas()
    fig = px.bar(
        df_p,
        x="jumlah",
        y="category",
        orientation="h",
        color="jumlah",
        color_continuous_scale="Blues",
        text="jumlah",
        title="<b>Top 15 Kategori Fasilitas dan POI Terbanyak di Indonesia</b><br><sup>Fasilitas pendidikan, ibadah, dan ritel modern mendominasi pemetaan digital</sup>",
        labels={"category": "Kategori Fasilitas", "jumlah": "Total Entitas"},
        template="plotly_white"
    )
    fig.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
    fig.update_layout(
        height=550,
        margin=dict(l=150, r=40, t=80, b=40),
        xaxis=dict(gridcolor=THEME_COLORS["grid"]),
        coloraxis_showscale=False
    )
    return fig


def plot_essential_facilities_comparison(amenity_df: pl.DataFrame) -> go.Figure:
    """
    Visualisasi 4: Komparasi Fasilitas Publik Esensial (Kesehatan vs Pendidikan vs Ibadah).
    """
    df_p = amenity_df.to_pandas()
    fig = px.bar(
        df_p,
        x="island",
        y="jumlah",
        color="sektor",
        barmode="group",
        title="<b>Distribusi Fasilitas Esensial Antar Wilayah: Pendidikan, Ibadah & Kesehatan</b><br><sup>Menunjukkan ketimpangan ketersediaan fasilitas layanan dasar di Indonesia Timur</sup>",
        labels={"island": "Wilayah", "jumlah": "Jumlah Fasilitas", "sektor": "Sektor Layanan"},
        color_discrete_map={
            "Pendidikan": "#1f77b4",
            "Ibadah": "#2ca02c",
            "Kesehatan": "#d62728",
            "Komersial": "#ff7f0e"
        },
        template="plotly_white"
    )
    fig.update_layout(
        height=500,
        yaxis=dict(gridcolor=THEME_COLORS["grid"]),
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5)
    )
    return fig


def plot_spatial_density_contour(sample_df: pl.DataFrame) -> go.Figure:
    """
    Visualisasi 5: Kontur Densitas Spasial 2D (Latitude vs Longitude Density).
    """
    df_p = sample_df.to_pandas()
    fig = px.density_contour(
        df_p,
        x="lon",
        y="lat",
        title="<b>Peta Kontur Densitas Klaster Spasial Indonesia</b><br><sup>Konsentrasi aglomerasi perkotaan Jabodetabek, Gerbangkertosusila, dan Medan</sup>",
        labels={"lon": "Bujur (Longitude °E)", "lat": "Lintang (Latitude °S/°N)"},
        template="plotly_white"
    )
    fig.update_traces(contours_coloring="fill", contours_showlabels=True, colorscale="Viridis")
    fig.update_layout(
        height=520,
        xaxis=dict(range=[94.0, 142.0], gridcolor=THEME_COLORS["grid"]),
        yaxis=dict(range=[-12.0, 7.0], gridcolor=THEME_COLORS["grid"])
    )
    return fig


def plot_temporal_mapping_trend(trend_df: pl.DataFrame) -> go.Figure:
    """
    Visualisasi 6: Tren Akumulasi Penambahan Entitas Spasial (Time Series dengan Range Slider).
    """
    df_p = trend_df.to_pandas()
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df_p["periode"],
        y=df_p["jumlah_baru"],
        mode="lines+markers",
        name="Penambahan Bulanan",
        line=dict(color="#1f77b4", width=2),
        marker=dict(size=4)
    ))
    
    fig.update_layout(
        title="<b>Dinamika Aktivitas Pemetaan Geospasial Indonesia (2018–2024)</b><br><sup>Peningkatan pesat terstimulasi oleh inisiatif Satu Data Indonesia dan digitalisasi infrastruktur</sup>",
        xaxis=dict(
            title="Waktu",
            rangeselector=dict(
                buttons=list([
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(count=3, label="3y", step="year", stepmode="backward"),
                    dict(step="all", label="Semua")
                ])
            ),
            rangeslider=dict(visible=True),
            type="date",
            gridcolor=THEME_COLORS["grid"]
        ),
        yaxis=dict(title="Jumlah Entitas Baru Terpetakan", gridcolor=THEME_COLORS["grid"]),
        height=520,
        template="plotly_white"
    )
    return fig


def plot_rolling_window_trend(rolling_df: pl.DataFrame) -> go.Figure:
    """
    Visualisasi 7: Polars Sliding Window Rolling Average & Volatilitas Pemetaan.
    """
    df_p = rolling_df.to_pandas()
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df_p["tanggal"],
        y=df_p["aktual"],
        mode="markers",
        name="Nilai Harian Aktual",
        marker=dict(color="#aec7e8", size=3, opacity=0.5)
    ))
    
    fig.add_trace(go.Scatter(
        x=df_p["tanggal"],
        y=df_p["rolling_mean"],
        mode="lines",
        name="Rata-rata Bergerak 30 Hari (Rolling Mean)",
        line=dict(color="#d62728", width=2.5)
    ))
    
    fig.add_trace(go.Scatter(
        x=df_p["tanggal"],
        y=df_p["rolling_upper"],
        mode="lines",
        name="Batas Atas (+2σ)",
        line=dict(color="#ff9896", dash="dot"),
        showlegend=False
    ))
    
    fig.add_trace(go.Scatter(
        x=df_p["tanggal"],
        y=df_p["rolling_lower"],
        mode="lines",
        name="Batas Bawah (-2σ)",
        line=dict(color="#ff9896", dash="dot"),
        fill="tonexty",
        fillcolor="rgba(255, 152, 150, 0.15)",
        showlegend=False
    ))
    
    fig.update_layout(
        title="<b>Analisis Deret Waktu Jendela Bergerak (Polars 30-Day Rolling Window)</b><br><sup>Filter noise harian mendeteksi tren musiman dan sprint pemetaan kontributor</sup>",
        xaxis=dict(title="Tanggal", gridcolor=THEME_COLORS["grid"]),
        yaxis=dict(title="Frekuensi Pemetaan", gridcolor=THEME_COLORS["grid"]),
        height=500,
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
    )
    return fig


def plot_osm_geometry_donut(geom_df: pl.DataFrame) -> go.Figure:
    """
    Visualisasi 8: Komposisi Tipe Geometri OpenStreetMap (Node, Way, Relation).
    """
    df_p = geom_df.to_pandas()
    fig = px.pie(
        df_p,
        names="osm_type",
        values="jumlah",
        hole=0.45,
        title="<b>Struktur Geometri Data OpenStreetMap Indonesia</b><br><sup>Dominasi node titik diskrit dibanding way (garis/poligon) dan relasi multi-elemen</sup>",
        color="osm_type",
        color_discrete_map={"node": "#1f77b4", "way": "#ff7f0e", "relation": "#2ca02c"},
        template="plotly_white"
    )
    fig.update_traces(textinfo="label+percent", pull=[0.05, 0, 0])
    fig.update_layout(height=450)
    return fig


def plot_window_ranking_by_island(rank_df: pl.DataFrame) -> go.Figure:
    """
    Visualisasi 9: Peringkat Windowing Fasilitas Terbanyak per Wilayah Pulau (DuckDB SQL DENSE_RANK).
    """
    df_p = rank_df.to_pandas()
    fig = px.bar(
        df_p,
        x="category",
        y="jumlah",
        color="island",
        barmode="group",
        facet_col="island",
        facet_col_wrap=3,
        title="<b>Ranking Kategori Fasilitas per Wilayah Menggunakan DuckDB Window Functions</b><br><sup>Top 5 kategori fasilitas teratas per pulau berdasarkan DENSE_RANK() OVER (PARTITION BY island)</sup>",
        labels={"category": "Kategori", "jumlah": "Jumlah"},
        template="plotly_white"
    )
    fig.update_layout(height=650, showlegend=False)
    fig.for_each_annotation(lambda a: a.update(text=f"<b>Pulau: {a.text.split('=')[-1]}</b>"))
    return fig


def export_all_figures(figures: Dict[str, go.Figure], output_dir: Path) -> None:
    """Mengekspor seluruh visualisasi interaktif ke direktori output/figures sebagai file HTML mandiri."""
    output_dir.mkdir(parents=True, exist_ok=True)
    for name, fig in figures.items():
        filepath = output_dir / f"{name}.html"
        fig.write_html(str(filepath), include_plotlyjs="cdn")
        print(f"Saved: {filepath.name}")
