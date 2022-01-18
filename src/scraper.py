import argparse
import json
from datetime import datetime, timedelta
from os import path as osp
import pandas as pd
import tweepy
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="example app")


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-q', help="query", type=str,
                        default="covid OR Pfizer-BioNTech OR pfizer OR moderna")
                        # default="covid OR Pfizer-BioNTech OR pfizer OR moderna OR Johnson&Johnson’s Janssen OR Johnson&Johnson")
    # parser.add_argument('-o', help="outfile", type=str)
    parser.add_argument('-c', help="count", type=int, default=500)
    return parser.parse_args()


def authenticate():
    #with open("keys.secret", "r") as f:
    #    keys = json.load(f)

    consumer_key = "bxgXriGEhN8HxMLlPcIx5OnMr"
    consumer_secret = "eGwi3XD2J1tUiK2b2kY4mPg4Ggxr2BWPtRRjnFYgA53qA4Ltxt"
    access_token = "4660324343-5KyMdN0u40JBJQ9bOMOhwl67Cz4nlm53OAJRFmu"
    access_token_secret = "09UYqNJJqVSrJC75fCkYinJ42HQT6fExgdAmPuiMQNeC9"
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    return api


def scrape(api, query, count, sinceDays, untilDays):
    # initial search

    since = (datetime.now() - timedelta(days=sinceDays)).strftime("%Y-%m-%d")
    until = (datetime.now() - timedelta(days=untilDays)).strftime("%Y-%m-%d")
    search = api.search_tweets(f"{query} -filter:retweets since:{since} until:{until}", lang="en", count=1,
                               tweet_mode='extended')  # , place_country="CA"
    oldest_id = search[0]._json["id_str"]
    print(f"Scraping from day {since} until day {until}")

    # write dataset
    # df = pd.DataFrame(columns=search[0]._json.keys())
    df = pd.DataFrame(columns=["id", "text", "url"])
    # df = df.append([search[0]._json["id"],search[0]._json["text"],search[0]._json["entities"]["urls"][0]["expanded_url"]], ignore_index=True)

    gotten = 0
    with open(osp.join("data", "scraped", "tweets" + ".json"), "w") as f:
        while gotten < count:

            search = api.search_tweets(f"{query} -filter:retweets since:{since} until:{until}", lang="en", count=count,
                                       max_id=oldest_id, tweet_mode='extended')  # , place_country="CA"
            for status in search:
                # location = geolocator.geocode(status._json["user"]["location"])
                # location and "Canada" in location.raw["display_name"] or
                if  any(place in status._json["user"]["location"] for place in
                        ["Canada", "Ontario", "Quebec", "British Columbia", "Nova Scotia", "Manitoba", "Alberta",
                         "New Brunswick", "Prince Edward Island", "Newfoundland and Labrador", "Saskatchewan"]) and not status._json["id"] in df["id"]:
                    print(status._json["user"]["location"])
                    f.write(json.dumps(status._json) + "\n")
                    # if len(status._json["entities"]["urls"]) == 0:
                    #     continue
                    df = df.append({"id": status._json["id"], "text": status._json["full_text"],
                                    "url": f"https://twitter.com/h24news_ie/status/{status._json['id']}"},
                                   ignore_index=True)
                    gotten += 1
                    if gotten % 100 == 0:
                        print(f"got {gotten} / {count}")

            if gotten >= count: break

            oldest_id = search[-1]._json["id"]

    #df.to_csv(osp.join("data", "scraped", "tweets.tsv"), sep="\t")
    print(f"Finished scraping from day {since} until day {until}")
    return df

def main():
    # parse arguments
    args = parse()
    # configure parser
    api = authenticate()
    # get tweets
    df = scrape(api, args.q, args.c, 3, 2)
    df = df.append(scrape(api, args.q, args.c, 4, 3), ignore_index=True)
    df = df.append(scrape(api, args.q, args.c, 5, 4), ignore_index=True)

    # remove any duplicates
    dropped = len(df) - len(df.drop_duplicates(['id','text','url'], keep='last'))
    print(f'Dropping {dropped} duplicates')
    df = df.drop_duplicates(['id','text','url'], keep='last')

    # check if got more than 1000 tweets, if not, scrape more.
    if len(df) < 1000:
        df = df.append(scrape(api, args.q, args.c, 5, 4), ignore_index=True)
        print("Scraped extra 500 posts.")
        dropped = len(df) - len(df.drop_duplicates(['id','text','url'], keep='last'))
        print(f'Dropping {dropped} duplicates')
        df = df.drop_duplicates(['id','text','url'], keep='last')

    print("Saving Dataframe to tweets.tsv")
    # dump df to a tsv file
    df.to_csv(osp.join("tweets.tsv"), sep="\t", index=False)
    print("Done.")

if __name__ == '__main__':
    main()
