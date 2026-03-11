import duckdb 
from pathlib import Path

CSV = "data/raw/LondonCrimeData.csv"
OUT = "data/processed/LondonCrimeData.parquet"

# create output path if missing
Path(OUT).parent.mkdir(parents=True, exist_ok=True)

duckdb.execute(f"""
    COPY (SELECT * FROM read_csv_auto('{CSV}'))
    TO '{OUT}' (FORMAT PARQUET)
""")