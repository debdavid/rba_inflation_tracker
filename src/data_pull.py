import pandas as pd
import requests
from io import BytesIO
from pathlib import Path

BRONZE = Path(__file__).parent.parent / "data" / "bronze"
BRONZE.mkdir(parents=True, exist_ok=True)


def pull_rba_cash_rate():
    url = "https://www.rba.gov.au/statistics/tables/xls/f01hist.xls"
    print(f"Downloading cash rate data from RBA...")

    response = requests.get(url, timeout=60)

    df = pd.read_excel(
        BytesIO(response.content),
        sheet_name="Data",
        skiprows=10,
        header=0
    )

    df.columns = [str(c).strip() for c in df.columns]
    df = df.dropna(how="all")

    save_path = BRONZE / "rba_cash_rate.parquet"
    df.to_parquet(save_path, index=False)

    print(f"Saved {len(df)} rows to {save_path.name}")
    return df


def pull_rba_mortgage_rates():
    url = "https://www.rba.gov.au/statistics/tables/xls/f05hist.xls"
    print(f"Downloading mortgage rate data from RBA...")

    response = requests.get(url, timeout=60)

    df = pd.read_excel(
        BytesIO(response.content),
        sheet_name="Data",
        skiprows=10,
        header=0
    )

    df.columns = [str(c).strip() for c in df.columns]
    df = df.dropna(how="all")

    save_path = BRONZE / "rba_mortgage_rates.parquet"
    df.to_parquet(save_path, index=False)

    print(f"Saved {len(df)} rows to {save_path.name}")
    return df


def pull_abs_cpi():
    url = "https://api.data.abs.gov.au/data/CPI/1.10001.10.50.Q"
    print(f"Downloading CPI data from ABS...")

    headers = {"Accept": "application/vnd.sdmx.data+json;version=1.0.0-wd"}
    response = requests.get(url, headers=headers, timeout=30)

    data = response.json()

    structure = data["data"]["structure"]
    dataset = data["data"]["dataSets"][0]

    time_periods = [
        p["id"] for p in structure["dimensions"]["observation"][0]["values"]
    ]

    rows = []
    for obs_key, obs_values in dataset["observations"].items():
        period_idx = int(obs_key.split(":")[0])
        value = obs_values[0]
        if value is not None:
            rows.append({
                "period": time_periods[period_idx],
                "cpi_value": float(value)
            })

    df = pd.DataFrame(rows)
    df["period"] = pd.to_datetime(df["period"])
    df = df.sort_values("period").reset_index(drop=True)

    save_path = BRONZE / "abs_cpi.parquet"
    df.to_parquet(save_path, index=False)

    print(f"Saved {len(df)} rows to {save_path.name}")
    return df


def pull_abs_wages():
    url = "https://api.data.abs.gov.au/data/WPI/1.1.3.Q"
    print(f"Downloading Wage Price Index from ABS...")

    headers = {"Accept": "application/vnd.sdmx.data+json;version=1.0.0-wd"}
    response = requests.get(url, headers=headers, timeout=30)

    data = response.json()

    structure = data["data"]["structure"]
    dataset = data["data"]["dataSets"][0]

    time_periods = [
        p["id"] for p in structure["dimensions"]["observation"][0]["values"]
    ]

    rows = []
    for obs_key, obs_values in dataset["observations"].items():
        period_idx = int(obs_key.split(":")[0])
        value = obs_values[0]
        if value is not None:
            rows.append({
                "period": time_periods[period_idx],
                "wpi_value": float(value)
            })

    df = pd.DataFrame(rows)
    df["period"] = pd.to_datetime(df["period"])
    df = df.sort_values("period").reset_index(drop=True)

    save_path = BRONZE / "abs_wages.parquet"
    df.to_parquest(save_path, index=False)

    print(f"Saved {len(df)} rows to {save_path.name}")
    return df

def pull_abs_unemployment():
    url = "https://api.data.abs.gov.au/data/LF/1.3.1599.20.M"
    print(f"Downloading unemployment data from ABS...")
    
    headers = {"Accept": "application/vnd.sdmx.data+json;version=1.0.0-wd"}
    response = requests.get(url, headers=headers, timeout=30)
    
    data = response.json()
    
    structure = data["data"]["structure"]
    dataset = data["data"]["dataSets"][0]
    
    time_periods = [
        p["id"] for p in structure["dimensions"]["observation"][0]["values"]
    ]
    
    rows = []
    for obs_key, obs_values in dataset["observations"].items():
        period_idx = int(obs_key.split(":")[0])
        value = obs_values[0]
        if value is not None:
            rows.append({
                "period": time_periods[period_idx],
                "unemployment_rate": float(value)
            })
            
    df = pd.DateFrame(rows)
    df["period"] = pd.to_datetime(df["period"])
    df = df.sort_values("period").reset_index(drop=True)
    
    save_path = BRONZE / "abs_unemployment.parquet"
    df.to_parquet(save_path, index=False)
    
    print(f"Saved {leb(df)} rows to {save_path.name}")
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