import os
import argparse
import os.path as osp
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

SENTS = ["Positive", "Neutral", "Negative"]
LABELS = ["Informative posts", "Informative questions", "Jokes and sarcasm", "Critique and opinions",
          "Compassion and sentiment", "Remove"]


# https://melaniewalsh.github.io/Intro-Cultural-Analytics/05-Text-Analysis/03-TF-IDF-Scikit-Learn.html#visualize-tf-idf
def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', help="query", type=str, default=osp.join('data', 'scraped', 'annotated-alon.tsv'))
    return parser.parse_args()


def plot(path):

    df = pd.read_csv(path, sep="\t", index_col=0)
    df = df[~df.category.str.contains("emptystring")]
    df = df[~df.category.str.contains("Remove")]
    df["text"] = 1
    print(df["sentiment"]=="Negative")
    outer = df.groupby('category').sum()
    inner = df.groupby(['category', 'sentiment']).sum()
    print(inner)

    inner_labels = inner.index.get_level_values(1)

    inner_colors = ["red", "yellow", "green"]*len(LABELS)
    fig, ax = plt.subplots(figsize=(24, 12))
    size = 0.3

    ax.pie(outer.values.flatten(), radius=1,
           labels=outer.index,
           autopct='%1.1f%%',
           wedgeprops=dict(width=size, edgecolor='w'))

    ax.pie(inner.values.flatten(), radius=1 - size,
           labels=inner_labels,
           wedgeprops=dict(width=size, edgecolor='w'), colors=inner_colors)

    ax.set(aspect="equal", title='Class Distribution')
    plt.show()


def main():
    args = parse()
    # open labeled data
    plot(args.i)


if __name__ == '__main__':
    main()
