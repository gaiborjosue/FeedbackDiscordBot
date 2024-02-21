import matplotlib.pyplot as plt
import io

def generateBarGraph(x, y, title, xlabel, ylabel):
    fig, ax = plt.subplots()
    x_positions = range(len(x))

    ax.bar(x_positions, y, color='blue', align='center')
    ax.set_xticks(x_positions)
    ax.set_xticklabels(x)  # Set the filtered grades as x-axis labels

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')

    buf.seek(0)

    return buf

