import polars as pl
from odu_ref_cc.utils import plot_by_year


def read_df(challenge: str):
    return pl.read_csv(f"odu-data/{challenge}/*.csv.gz", has_header=True, separator=";")
