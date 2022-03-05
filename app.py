# Import dependecies
from utils import call_spotify_db, call_twitter_db
from flask import Flask, jsonify, render_template, request
from flask import redirect, jsonify
import pandas as pd
from sqlalchemy import create_engine, func
import json


connection_string = "postgres:Dontforget123!@localhost:5432/twitter_sentiments"
engine = create_engine("postgresql://" + connection_string)
#engine = create_engine(f'postgresql://{connection_string}')
app = Flask(__name__)


@app.route("/")
def index():
    spotify_dbs = pd.read_sql('select * from spotifydb', engine).to_dict()
    return render_template('index.html', spotify_dbs=spotify_dbs['genre'].values(), twitter_handle="twitter_handle", data={})


@app.route("/twitter-analysis/<twitter_handle>/")
def sentiment_analysis():
    twitter_handle = request.get("twitter-handle")
    return print_name(twitter_handle)


@app.route("/humming-bird/")
def twitter_sentiments_route():
    twitter_handle = request.args.get("twitter_handle")
    twitter_df = call_twitter_db(twitter_handle)
    spotify_df = call_spotify_db()

    twitter_df.Sentiment.value_counts()

    Sentiment = twitter_df.Sentiment.value_counts().to_dict()
    Sentiment = max(Sentiment, key=Sentiment.get)

    print("Your Tweets look really "+Sentiment+"!")

    data = spotify_df[(spotify_df["sentiment"] == Sentiment)].T.to_dict()
    return render_template("humming-bird.html", data=data)


@app.route('/playlist')
def playlist():
    spotify_db = pd.read_sql('select * from spotifydb', engine)
    spotify_db = spotify_db[spotify_db["sentiment"] == "Positive"]
  # return render_template("spotify_playlist.html",title="twitter_sentiment_playlist",rows=rows)
    return spotify_db.T.to_dict()


if __name__ == "__main__":
    app.run(debug=True)
