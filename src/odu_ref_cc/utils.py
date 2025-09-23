import os


def plot_by_year(dataframe, col_name):
    import matplotlib.pyplot as plt

    _, ax = plt.subplots()
    ax.scatter(
        x=dataframe["year"],
        y=dataframe[col_name],
    )
    ax.set_title("test")
    ax.set_xlabel("date")
    ax.set_ylabel(col_name)
    plt.show()
