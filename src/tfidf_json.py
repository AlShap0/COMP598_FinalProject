from sklearn.feature_extraction.text import TfidfVectorizer
import argparse
import os.path as osp
import pandas as pd
import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import json

SENTS = ["Positive", "Neutral", "Negative"]
LABELS = ["Informative posts", "Informative questions", "Jokes and sarcasm", "Critique and opinions",
          "Compassion and sentiment", "Remove"]


# https://melaniewalsh.github.io/Intro-Cultural-Analytics/05-Text-Analysis/03-TF-IDF-Scikit-Learn.html#visualize-tf-idf
def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', help="query", type=str, default=osp.join('data', 'scraped', 'final_data.tsv'))
    return parser.parse_args()


def tokenize(post):
    # print(stop_words)
    stemmer = PorterStemmer()
    stop_words = set([stemmer.stem(word) for word in stopwords.words('english') + ["http", 'amp', 'like', 'one', 'today', 'jatetro', 'dress', 'even', 'say', 'would', 'also', 'got', 'much', 'first', 'go']])
    words = [stemmer.stem(word) for word in nltk.word_tokenize(post) if
             stemmer.stem(word) not in stop_words and word.isalnum() and not word.isdecimal()]
    return words


def compute_top_tfidf(df, output, categories, column):
    documents = []
    for sentiment in categories:
        words = ""
        for line in df[df[column] == sentiment]["text"]:
            for word in line.split():
                words += f" {word}"
        documents.append(words)

    vectorizer = TfidfVectorizer(tokenizer=tokenize)
    tfidf_df = pd.DataFrame(vectorizer.fit_transform(documents).toarray(), index=categories,
                            columns=vectorizer.get_feature_names())
    top_df = tfidf_df.apply(lambda s: s.abs().nlargest(11).index.tolist(), axis=1)

    highest_dict = {} # dict will store all category titles and their top 10 tf-idf word and values
    for i, row in tfidf_df.iterrows():
        print(i, row.sort_values(ascending=False).head(11))
        highest_dict[i] = row.sort_values(ascending=False).head(11).to_dict()

    top_df.to_csv(output)

    # output to file
    jsonString = json.dumps(highest_dict, indent = 4)
    jsonFile = open(f'{column}.json', "w")
    jsonFile.write(jsonString)
    jsonFile.close()

    #print(top_df)


def main():
    args = parse()
    # open labeled data
    df = pd.read_csv(args.i, sep="\t")#, index_col=0)

    compute_top_tfidf(df, "top_sentiment.csv", SENTS, "sentiment")

    compute_top_tfidf(df, "top_categories.csv", LABELS, "category")


if __name__ == '__main__':
    main()
