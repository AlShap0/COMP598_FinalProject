import pandas as pd
import json
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import argparse

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--input_cat') # path to input file
    parser.add_argument('-s', '--input_sent')

    args = parser.parse_args()
    inputCat = args.input_cat
    inputSent = args.input_sent


    f = open(inputCat)

    cat_idf = json.load(f)
    f.close()

    f = open(inputSent)
    sent_idf = json.load(f)
    f.close()

    cat_idf.pop('Remove')

    for key in cat_idf:
        cat_idf[key].pop('covid')

    for key in sent_idf:
        sent_idf[key].pop('covid')


    #plt.figure(figsize=(10,12), dpi = 500)
    fig, axes = plt.subplots(4, 2, sharex=True, figsize=(8,12), dpi=500)

    fig.suptitle('td-idf values for each category')

    ax1 = sns.barplot(ax=axes[0, 0], data=pd.DataFrame(cat_idf)[['Informative posts']].dropna().T.sort_values(by='Informative posts', axis=1, ascending=False), orient='h', color='salmon')
    ax1.set(title="Informative posts")
    ax1.grid(visible=True, axis='both')

    ax2 = sns.barplot(ax=axes[0, 1], data=pd.DataFrame(cat_idf)[['Informative questions']].dropna().T.sort_values(by='Informative questions', axis=1, ascending=False), orient='h', color='navajowhite')
    ax2.set(title="Informative questions")
    ax2.grid(visible=True, axis='both')

    ax3 = sns.barplot(ax=axes[1, 0], data=pd.DataFrame(cat_idf)[['Jokes and sarcasm']].dropna().T.sort_values(by='Jokes and sarcasm', axis=1, ascending=False), orient='h', color='lightgreen')
    ax3.set(title="Jokes and sarcasm")
    ax3.grid(visible=True, axis='both')

    ax4 = sns.barplot(ax=axes[1,1], data=pd.DataFrame(cat_idf)[['Critique and opinions']].dropna().T.sort_values(by='Critique and opinions', axis=1, ascending=False), orient='h', color='cornflowerblue')
    ax4.set(title="Critique and opinions")
    ax4.grid(visible=True, axis='both')

    ax5 = sns.barplot(ax=axes[2,0],data=pd.DataFrame(cat_idf)[['Compassion and sentiment']].dropna().T.sort_values(by='Compassion and sentiment', axis=1, ascending=False), orient='h', color='gold')
    ax5.set(title="Compassion and sentiment")
    ax5.grid(visible=True, axis='both')

    ax6 = sns.barplot(ax=axes[2,1],data=pd.DataFrame(sent_idf)[['Positive']].dropna().T.sort_values(by='Positive', axis=1, ascending=False), orient='h', color='darkgray')
    ax6.set(title="Positive sentiment")
    ax6.grid(visible=True, axis='both')

    ax7 = sns.barplot(ax=axes[3,0],data=pd.DataFrame(sent_idf)[['Negative']].dropna().T.sort_values(by='Negative', axis=1, ascending=False), orient='h', color='blueviolet')
    ax7.set(title="Negative sentiment", xlabel='td-idf value')
    ax7.grid(visible=True, axis='both')

    ax8 = sns.barplot(ax=axes[3,1],data=pd.DataFrame(sent_idf)[['Neutral']].dropna().T.sort_values(by='Neutral', axis=1, ascending=False), orient='h', color='pink')
    ax8.set(title="Neutral sentiment", xlabel='td-idf value')
    ax8.grid(visible=True, axis='both')

    plt.tight_layout()
    plt.savefig('tf-idf_fig.jpeg')
    plt.show()

if __name__ == '__main__':
    main()
