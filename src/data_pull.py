import pandas as pd
from pathlib import Path

BRONZE = Path(__file__).parent.parent / "data" / "bronze"
BRONZE.mkdir(parents=True, exist_ok=True)


def pull_rba_cash_rate():
    file_path = BRONZE / "rba_cash_rate.xlsx"
    print("Reading cash rate data from local file...")
    df = pd.read_excel(file_path, sheet_name="Data",
                       skiprows=10, header=0, engine="openpyxl")
    df.columns = [str(c).strip() for c in df.columns]
    df = df.dropna(how="all")
    df.to_parquet(BRONZE / "rba_cash_rate.parquet", index=False)
    print(f"Saved {len(df)} rows to rba_cash_rate.parquet")
    return df


def pull_rba_mortgage_rates():
    file_path = BRONZE / "rba_mortgage_rates.xlsx"
    print("Reading mortgage rate data from local file...")
    df = pd.read_excel(file_path, sheet_name="Data",
                       skiprows=10, header=0, engine="openpyxl")
    df.columns = [str(c).strip() for c in df.columns]
    df = df.dropna(how="all")
    df.to_parquet(BRONZE / "rba_mortgage_rates.parquet", index=False)
    print(f"Saved {len(df)} rows to rba_mortgage_rates.parquet")
    return df


def pull_abs_cpi():
    file_path = BRONZE / "abs_cpi.xlsx"
    print("Reading CPI data from local file...")
    xl = pd.ExcelFile(file_path, engine="openpyxl")
    print(f"Sheets available: {xl.sheet_names}")
    df = xl.parse(xl.sheet_names[0])
    df.to_csv(BRONZE / "abs_cpi.csv", index=False)
    print(f"Saved {len(df)} rows to abs_cpi.csv")
    return df


def pull_abs_wages():
    file_path = BRONZE / "abs_wages.xlsx"
    print("Reading wages data from local file...")
    xl = pd.ExcelFile(file_path, engine="openpyxl")
    print(f"Sheets available: {xl.sheet_names}")
    df = xl.parse(xl.sheet_names[0])
    df.to_csv(BRONZE / "abs_wages.csv", index=False)
    print(f"Saved {len(df)} rows to abs_wages.csv")
    return df


def pull_abs_unemployment():
    file_path = BRONZE / "abs_unemployment.xlsx"
    print("Reading unemployment data from local file...")
    xl = pd.ExcelFile(file_path, engine="openpyxl")
    print(f"Sheets available: {xl.sheet_names}")
    df = xl.parse(xl.sheet_names[0])
    df.to_csv(BRONZE / "abs_unemployment.csv", index=False)
    print(f"Saved {len(df)} rows to abs_unemployment.csv")
    return df

def pull_all():
    print("\n" + "="*50)
    print("RBA Inflation Tracker - Pulling All Data")
    print("="*50 + "\n")
    pull_rba_cash_rate()
    pull_rba_mortgage_rates()
    pull_abs_cpi()
    pull_abs_wages()
    pull_abs_unemployment()
    print("\n" + "="*50)
    print("All data pulled successfully.")
    print("="*50 + "\n")


if __name__ == "__main__":
    pull_all()