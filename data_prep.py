import pandas as pd

def load_data():
    df = pd.read_csv("data/Crimes_-_2001_to_Present_20260406.csv")
    df = df[df["Year"] == 2025].copy()
    df["Date"] = pd.to_datetime(df["Date"])
    df["Month"] = df["Date"].dt.month
    df["Hour"] = df["Date"].dt.hour
    df["DayOfWeek"] = df["Date"].dt.day_name()
    df = df.dropna(subset=["Latitude", "Longitude"])
    return df