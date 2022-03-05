# Import dependecies
from utils import call_spotify_db, call_twitter_db
from flask import Flask, jsonify, render_template, request
from flask import Flask, render_template, redirect, jsonify
import pandas as pd
from sqlalchemy import create_engine, func
import json


connection_string = "postgres:12345@localhost:5432/twitter_sentiments"
engine = create_engine(f'postgresql://{connection_string}')
app = Flask(__name__)


@app.route("/")
def index():
    # teams_table = list(engine.execute("select * from seasons"))
    spotify_dbs = pd.read_sql('select * from spotifydb', engine).to_dict()
    return render_template('index.html', spotify_dbs=spotify_dbs['genre'].values(), twitter_handle="twitter_handle", data={})


@app.route("/twitter-analysis/<twitter_handle>/")
def sentiment_analysis():
    twitter_handle=request.get("twitter-handle")
    return print_name(twitter_handle)


@app.route("/humming-bird/")
def twitter_sentiments_route():
    twitter_handle=request.args.get("twitter_handle")
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

   # return str(process_sum())
   # return jsonify(process_number_2())
   # return process_number_2()
if __name__ == "__main__":
    app.run(debug=True)


#     try:
#         songs = twitter_sentiments.query.filter_by(sentiment= 'Positive').order_by(twitter_sentiments.sentiment).all()
#         songs_text = '<ul>'
#         for song in songs:
#             songs_text += '<li>' + song.sentiment + ', ' + song.track + '</li>'
#         songs_text += '</ul>'
#         return songs_text
#     except Exception as e:
#         # e holds description of the error
#         error_text = "<p>The error:<br>" + str(e) + "</p>"
#         hed = '<h1>Something is broken.</h1>'
#         return hed + error_text


@app.route("/twitter-analysis/<twitter_handle>/")
def twitter_sentiments_route(twitter_handle):
    return twitter_mood(twitter_handle)
    #spotify_db = pd.read_sql('select * from spotifydb', engine).to_dict()
    # return render_template('index.html',spotify_db=spotify_db)
    #playlist = []

    # for i in spotify_db:
    # return(i[2])
    # if tweetmood == 'positive'

    # playlist.append(tracks  where sentiment  == "positive")
    # return playlist


if __name__ == '__main__':
    app.run(debug=True)
