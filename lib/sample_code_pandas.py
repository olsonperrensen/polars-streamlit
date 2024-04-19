import pandas as pd
import matplotlib.pyplot as plt


def explore_data(data):
    print("Shape of the DataFrame:")
    print(data.shape)

    print("Data Types:")
    print(data.dtypes)

    print("Head of the DataFrame:")
    print(data.head())

    print("Description of the DataFrame:")
    print(data.describe())

    print("Missing Values:")
    print(data.isnull().sum())


def plot_data(data):

    print("Scatterplot of first two columns:")
    data.plot(kind="scatter", x=data.columns[0], y=data.columns[1])
    plt.show()

    print("Histogram of first column:")
    data[data.columns[0]].hist()
    plt.show()

    print("Barplot of first categorical column:")
    data[data.columns[1]].value_counts().plot(kind="bar")
    plt.show()

    # Generate dummy data
    data = pd.DataFrame(
        {
            "A": [1, 2, 3, 4, 5],
            "B": ["a", "b", "c", "d", "e"],
            "C": [10.0, 20.0, 30.0, 40.0, 50.0],
            "D": [True, False, True, False, True],
        }
    )

    # Explore the data
    explore_data(data)

    # Plot the data
    plot_data(data)
