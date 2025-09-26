import polars as pl
from odu_ref_cc.utils import plot_by_year

CRS_LAMBERT_2 = 27572


def read_df(challenge: str):
    return pl.read_csv(f"odu-data/{challenge}/*.csv.gz", has_header=True, separator=";")


def get_france_map():
    from cartiflette import carti_download

    map = carti_download(
        values=["France"],
        crs=4326,
        borders="DEPARTEMENT",
        vectorfile_format="geojson",
        filter_by="FRANCE_ENTIERE_DROM_RAPPROCHES",
        source="EXPRESS-COG-CARTO-TERRITOIRE",
        year=2022,
    )
    map = map.to_crs(CRS_LAMBERT_2)
    return map
