import matplotlib.pyplot as plt
import io

def generateBarGraph(x, y, title, xlabel, ylabel, background_color, bar_color, label_color):
    fig, ax = plt.subplots()

    fig.patch.set_facecolor(background_color)
    ax.set_facecolor(background_color)

    x_positions = range(len(x))

    ax.bar(x_positions, y, color=f'{bar_color}', align='center')
    ax.set_xticks(x_positions)
    ax.set_xticklabels(x, color=f'{label_color}')  # Set the filtered grades as x-axis labels

    plt.xlabel(xlabel, color=f'{label_color}')
    plt.ylabel(ylabel, color=f'{label_color}')
    plt.title(title, color=f'{label_color}')

    for spine in ax.spines.values():
        spine.set_color(f'{label_color}')

    ax.tick_params(colors=f'{label_color}', which='both')

    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')

    buf.seek(0)

    return buf

