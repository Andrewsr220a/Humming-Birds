# Import dependecies
from flask import Flask, render_template, redirect, jsonify
from utils import twitter_mood
import pandas as pd
from sqlalchemy import create_engine,func



connection_string = "postgres:postgress@localhost:5432/twitter_sentiments"
engine = create_engine(f'postgresql://{connection_string}')
app = Flask(__name__)


@app.route("/")
def index():
    # teams_table = list(engine.execute("select * from seasons"))
    spotify_dbs = pd.read_sql('select * from spotifydb', engine).to_dict()
    return render_template('index.html',spotify_dbs=spotify_dbs['genre'].values(),handle="JoeBiden")


@app.route('/playlist')
def playlist():
    spotify_db = pd.read_sql('select * from spotifydb', engine)
    spotify_db=spotify_db[spotify_db["sentiment"]=="Positive"]
  # return render_template("spotify_playlist.html",title="twitter_sentiment_playlist",rows=rows)
    return spotify_db.T.to_dict()
    
    
    
    
    
    
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
    #return render_template('index.html',spotify_db=spotify_db)
    #playlist = []
    
    #for i in spotify_db:
        #return(i[2])
        #if tweetmood == 'positive'
        
        #playlist.append(tracks  where sentiment  == "positive")
        #return playlist

if __name__ == '__main__':
    app.run(debug=True)
    



