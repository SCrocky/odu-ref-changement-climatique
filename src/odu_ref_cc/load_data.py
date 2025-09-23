import polars as pl
from utils import plot_by_year

df = pl.read_csv("data/MENS_SIM2_*.csv.gz", has_header=True, separator=";")
df = df.with_columns(
    pl.col("DATE").cast(pl.String).str.slice(0, 4).alias("year"),
    pl.concat_str(
        pl.col("LAMBX").cast(pl.String), pl.col("LAMBY").cast(pl.String), separator=":"
    ).alias("location"),
)
df2 = df.group_by("year").agg(
    pl.col("T_MENS").mean().alias("avg_tmp"),
    pl.col("PRELIQ_MENS").mean().alias("avg_rain"),
    pl.col("PE_MENS").mean().alias("avg_eff_rain"),
)

df2 = df2.sort("year")

df_stations = (
    df.group_by("year")
    .agg(pl.col("location").n_unique().alias("distinct_locations"))
    .sort("year")
)

plot_by_year(df2, "avg_tmp")
plot_by_year(df2, "avg_rain")
plot_by_year(df2, "avg_eff_rain")
plot_by_year(df_stations, "distinct_locations")
