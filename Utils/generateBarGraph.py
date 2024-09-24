import matplotlib.pyplot as plt
import io
import math

def generateBarGraph(x, y, title, xlabel, ylabel, background_color, bar_color, label_color):
    int_y = range(math.floor(min(y)), math.ceil(max(y))+1)

    fig, ax = plt.subplots()

    fig.patch.set_facecolor(background_color)
    ax.set_facecolor(background_color)

    x_positions = range(len(x))

    ax.bar(x_positions, y, color=f'{bar_color}', align='center')
    ax.set_xticks(x_positions)
    ax.set_xticklabels(x, color=f'{label_color}')  # Set the filtered grades as x-axis labels

    plt.yticks(int_y, color=f'{label_color}')
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


def generatePointGraph(x, y, title, xlabel, ylabel, background_color, point_color, label_color):    
    int_y = range(math.floor(min(y)), math.ceil(max(y))+1)
    int_x = range(math.floor(min(x)), math.ceil(max(x))+1)
    
    fig, ax = plt.subplots()

    fig.patch.set_facecolor(background_color)
    ax.set_facecolor(background_color)

    ax.plot(x, y, color=f'{point_color}'
            , marker='o'
            , markersize=5
            , linestyle='solid'
            , linewidth=1)

    plt.yticks(int_y, color=f'{label_color}')
    plt.xticks(int_x, color=f'{label_color}')

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