import pandas as pd


def get_daily_time(data: pd.DataFrame) -> pd.Series:
    return data.groupby("Date")[
        "Time (min)"
    ].sum()  # get how much time was spent on productivity each day


def get_mood_trend(data: pd.DataFrame) -> pd.Series:
    return data.groupby("Date")["Mood (1-5)"].mean()  # get the average mood each day


def get_category_breakdown(data: pd.DataFrame) -> pd.Series:
    return data.groupby("Category")[
        "Time (min)"
    ].sum()  # breakdowns how much time was spent on each category
