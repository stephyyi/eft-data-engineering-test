"""
transformation logic for EFT transactions pipeline
"""


import pandas as pd


def validate_and_clean(df: pd.DataFrame) -> pd.DataFrame:
    """cleans nulls, validates types, filters bad data."""
    # Drop completely null rows
    df = df.dropna(how="all")

    # Ensure column types
    expected_types = {
        "transaction_id": str,
        "bank_id": str,

        "customer_id": str,
        "amount": float,
        "timestamp": "datetime64[ns]"
    }

    for col, dtype in expected_types.items():
        if col in df.columns:
            try:
                df[col] = df[col].astype(dtype)
            except Exception:
                if dtype == "datetime64[ns]":
                    df[col] = pd.to_datetime(df[col], errors="coerce")
                else:
                    df[col] = pd.to_numeric(df[col], errors="coerce")

    # Drop rows with null critical values
    df = df.dropna(subset=["transaction_id", "bank_id", "amount", "timestamp"])

    # Remove negative or zero amounts
    df = df[df["amount"] > 0]

    return df


def aggregate_daily_by_bank(df: pd.DataFrame) -> pd.DataFrame:
    """aggregates daily totals by bank_id."""
    df["txn_date"] = df["timestamp"].dt.date

    agg = (
        df.groupby(["txn_date", "bank_id"])
        .agg(
            total_volume=("amount", "count"),
            total_value=("amount", "sum"),
            avg_value=("amount", "mean"),
            median_value=("amount", "median"),
        )
        .reset_index()
    )
    return agg


def transform_file(input_csv: str, output_csv: str):
    """CLI wrapper for standalone transformation."""
    df = pd.read_csv(input_csv, parse_dates=["timestamp"])
    df = validate_and_clean(df)
    agg = aggregate_daily_by_bank(df)
    agg.to_csv(output_csv, index=False)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Transform transaction data")
    parser.add_argument("--in", dest="input_csv", required=True)
    parser.add_argument("--out", dest="output_csv", required=True)
    args = parser.parse_args()

    transform_file(args.input_csv, args.output_csv)
