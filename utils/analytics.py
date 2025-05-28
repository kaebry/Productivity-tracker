import pandas as pd


def get_daily_time(data: pd.DataFrame) -> pd.Series:
    return data.groupby("Date")["Time (min)"].sum()


def get_mood_trend(data: pd.DataFrame) -> pd.Series:
    return data.groupby("Date")["Mood (1-5)"].mean()


def get_category_breakdown(data: pd.DataFrame) -> pd.Series:
    return data.groupby("Category")["Time (min)"].sum()
