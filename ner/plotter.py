import os
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter


def calculate_data(kind, ents):
    if kind == 'summary':
        return ['People', 'Organization', 'Location'], [len(ents.get('PERSON', [])), len(ents.get('ORG', [])), len(ents.get('GPE', []))]
    if kind == 'detailed':
        people = Counter(ents.get('PERSON', [])).most_common(3)
        organization = Counter(ents.get('ORG', [])).most_common(3)
        location = Counter(ents.get('GPE', [])).most_common(3)
        xs = []
        ys = []
        for p in people:
            xs.append(f"{p[0]} - People")
            ys.append(p[1])
        for o in organization:
            xs.append(f"{o[0]} - Organization")
            ys.append(o[1])
        for l in location:
            xs.append(f"{l[0]} - Location")
            ys.append(l[1])

        return xs, ys


def plot(ents, kind, date, name):
    xs, ys = calculate_data(kind, ents)

    x = np.arange(len(xs))  # the label locations
    width = 0.35  # the width of the bars

    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(111)
    rects1 = ax.bar(x, ys, width)

    #for index, rect in enumerate(rects1):
        #rect.set_color(get_color(index, kind))

    ax.set_title(f"{name} - {kind.capitalize()}")
    ax.set_xticks(x)
    ax.set_xticklabels(xs)
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=80)
    autolabel(ax, rects1)
    fig.tight_layout()
    fig1 = plt.gcf()
    plt.grid()
    plt.show()
    fig1.savefig(filepath(kind, date, name), dpi=200)


def filepath(kind, date, name):
    directory_path = f"/home/marco/Scrivania/tirocinio-unicredit/ner/plots/{date}/{name}"
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    return f"{directory_path}/{kind}.png"


def get_color(index, kind):
    if kind == 'summary':
        return 'blue'
    if index in [0, 1, 2]:
        return 'green'
    if index in [3, 4, 5]:
        return 'red'
    if index in [6, 7, 8]:
        return 'yellow'


def autolabel(ax, rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')
