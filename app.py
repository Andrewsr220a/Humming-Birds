# Import dependecies
from flask import Flask, render_template, redirect, jsonify
from utils import twitter_sentiments
import pandas as pd
from sqlalchemy import create_engine,func


connection_string = "postgres:postgress@localhost:5432/twitter_sentiments"
engine = create_engine(f'postgresql://{connection_string}')
app = Flask(__name__)


@app.route("/")
def index():
    # teams_table = list(engine.execute("select * from seasons"))
    spotify_db = pd.read_sql('select genre from spotifydb', engine).to_dict()
    return render_template('index.html',spotify_db=spotify_db['genre'].values())
    
@app.route("/twitter-analysis/<twitter_handle>/")
def twitter_sentiments(twitter_handle):   
    return twitter_sentiments("getAnalysis")

if __name__ == '__main__':
    app.run(debug=True)
    
