import matplotlib.pyplot as plt
import os
import json
import numpy as np
import settings


def tweets(kind, date):
    informations = []
    tweets = []
    directory = f"{settings.TWEETS_DATA_FOLDER}{kind}/{date}"
    for filename in os.listdir(directory):
        file = open(directory + '/' + filename)
        parsed_file = json.load(file)
        informations.append(filename.split('.')[0])
        tweets.append(parsed_file['meta']['result_count'])

    x = np.arange(len(tweets))  # the label locations
    width = 0.35  # the width of the bars

    fig = plt.figure(figsize=(20, 7))
    ax = fig.add_subplot(111)
    rects1 = ax.bar(x, tweets, width)

    ax.set_title(f"{kind.capitalize()} Tweets")
    ax.set_xticks(x)
    ax.set_xticklabels(informations)
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=80)
    autolabel(ax, rects1)
    fig.tight_layout()
    fig1 = plt.gcf()
    plt.grid()
    plt.show()
    fig1.savefig(filepath(kind, date), dpi=200)


def filepath(kind, date):
    directory_path = f"{settings.PLOTS_FOLDER}{date}"
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    return f"{directory_path}/{kind}.png"


def autolabel(ax, rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')
