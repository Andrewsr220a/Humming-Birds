# Import the Libraries
from cgitb import text
from textblob import TextBlob, Word, Blobber
from wordcloud import WordCloud
import tweepy
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import json
from flask import Flask, render_template, redirect, jsonify
from sqlalchemy import create_engine, func

app = Flask(__name__)


def call_twitter_db(twitter_handle):
    file_path = "/Users/raishandrews/Documents/GitHub/Humming-Birds/config.json"
    with open(file_path) as fp:
        config = json.loads(fp.read())

    print(config['KEY'])

    # Twitter Api Cred.
    key = (config['KEY'])
    secret = (config['SECRET'])
    bear = (config['BEAR'])
    token = (config['ACC_TOKE'])
    token_secr = (config['ACC_SECR'])

    # Creating the auth object
    auth = tweepy.OAuthHandler(key, secret)
    # Setting token and access secret
    auth.set_access_token(token, token_secr)
    # Creating the api call
    api = tweepy.API(auth, wait_on_rate_limit=True)

    # Testing Tweet call
    post = api.user_timeline(screen_name=twitter_handle,
                             count=100, lang="en", tweet_mode="extended")

    # Print 10 tweets
    i = 1
    print("Showing the 10 most recent tweets: \n")
    for tweet in post[0:10]:
        print(str(i) + ")" + tweet.full_text + "\n")
    i = i + 1

    df = pd.DataFrame([tweet.full_text for tweet in post], columns=["Tweets"])

    df.head(11)

    def cleanTxt(text):
        #removing @mentions
        text = re.sub('@[A-Za-z0-9]+', '', text)
    # Removing the "#" symbol
        text = re.sub(r"#", "", text)
    # Removing RT
        text = re.sub(r"RT[\s]+", '', text)
    # Remove the hyper link
        text = re.sub(r"https?:\/\/S+", '', text)
        return text

    # Cleaned tweets down to just text
    df['Tweets'] = df['Tweets'].apply(cleanTxt)

    # Getting the subjectivity telling how opinionated the tweet is

    def getSubjectivity(text):
        return TextBlob(text).sentiment.subjectivity

    # Get polarity to tell how positive or negative tweet is
    def getPolarity(text):
        return TextBlob(text).sentiment.polarity

    # Adding columns for subjectivity and polarity
    df['Subjectivity'] = df['Tweets'].apply(getSubjectivity)

    df['Polarity'] = df['Tweets'].apply(getPolarity)

    def getAnalysis(score):
        if score < 0:
            return 'Negative'
        elif score == 0:
            return 'Neutral'
        else:
            return 'Positive'

    df['Sentiment'] = df['Polarity'].apply(getAnalysis)

    df.Sentiment.value_counts()

    Sentiment = df.Sentiment.value_counts().to_dict()
    Sentiment = max(Sentiment, key=Sentiment.get)

    print("Your Tweets look really "+Sentiment+"!")

    return df[(df["Sentiment"] == Sentiment)]


def call_spotify_db():
    connection_string = "postgres:Dontforget123!@localhost:5432/twitter_sentiments"
    engine = create_engine("postgresql://" + connection_string)
    # engine = create_engine(f'postgresql://{connection_string}')
    spotify_df = pd.read_sql('select * from spotifydb', engine)
    return spotify_df
