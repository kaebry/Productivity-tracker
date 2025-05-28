import matplotlib.pyplot as plt
import pandas as pd


def plot_category_bar(category_data: pd.Series):
    fig, ax = plt.subplots()
    category_data.plot(kind="bar", ax=ax, color="skyblue")
    ax.set_title("Time Spent by Category")
    ax.set_ylabel("Time (min)")
    ax.set_xlabel("Category")
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig
