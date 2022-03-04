#Import the Libraries 
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


def twitter_mood(twitter_handle):

    file_path= "/Users/prajesh/Desktop/Class_Activity/Project4/config.json"
    with open(file_path) as fp:
        config = json.loads(fp.read())

    print(config['KEY'])

    # Twitter Api Cred.
    key = (config['KEY'])
    secret = (config['SECRET'])
    bear= (config['BEAR'])
    token= (config['ACC_TOKE'])
    token_secr= (config['ACC_SECR'])

    #Creating the auth object
    auth = tweepy.OAuthHandler(key, secret)
    #Setting token and access secret 
    auth.set_access_token(token, token_secr)
    #Creating the api call 
    api = tweepy.API(auth, wait_on_rate_limit=True)

    #Testing Tweet call
    post = api.user_timeline(screen_name= twitter_handle, count = 100, lang= "en", tweet_mode = "extended")

    #Print 10 tweets
    i = 1
    print("Showing the 10 most recent tweets: \n")
    for tweet in post [0:10]:
        print( str(i) + ")" + tweet.full_text + "\n")
    i = i +1
    
    df = pd.DataFrame([tweet.full_text for tweet in post], columns=["Tweets"])

    df.head(11)

    def cleanTxt(text):
        #removing @mentions
        text = re.sub('@[A-Za-z0-9]+', '', text)
    #Removing the "#" symbol 
        text = re.sub(r"#", "",text)
    #Removing RT
        text = re.sub(r"RT[\s]+",'',text)
    #Remove the hyper link
        text = re.sub(r"https?:\/\/S+",'',text)
        return text

    #Cleaned tweets down to just text  
    df['Tweets']= df['Tweets'].apply(cleanTxt)

    #Show the cleaned text
   # df=df.dropna()

    #Getting the subjectivity telling how opinionated the tweet is 
    def getSubjectivity(text):
        return TextBlob(text).sentiment.subjectivity

    #Get polarity to tell how positive or negative tweet is 
    def getPolarity(text):
        return TextBlob(text).sentiment.polarity

    # Adding columns for subjectivity and polarity
    df['Subjectivity']  = df['Tweets'].apply(getSubjectivity)

    df['Polarity'] = df['Tweets'].apply(getPolarity)

    #updated dataframe
   # 

    # Visualizing using the WordCloud
    all_words = " ".join( [twts for twts in df['Tweets']])
    #wordCloud = WordCloud(width = 600, height = 400, random_state = 20, max_font_size = 120 ).generate(all_words)

    #plt.imshow(wordCloud, interpolation= "bilinear")
    #plt.axis("off")
    #plt.show()

    # Creating a function that can compute negative, neutral and positive anlysis
    def getAnalysis(score):
        if score < 0:
            return 'Negative'
        elif score == 0:
            return 'Neutral'
        else:
            return 'Positive'

    df['Sentiment']= df['Polarity'].apply(getAnalysis)

    #updated dataframe

    #Print positive tweets 

    j= 1
    PositiveDF = df.sort_values(by=['Polarity'])
    for i in range(0, PositiveDF.shape[0]):
        if(PositiveDF['Sentiment'][i] == 'Positive'):
            print(str(j) + ')' + PositiveDF['Tweets'][i])
        print()
        j = j+i
        
    #Print Negative tweets 

    j= 1
    NegativeDF = df.sort_values(by=['Polarity'], ascending= 'False')
    for i in range(0, NegativeDF .shape[0]):
        if(NegativeDF ['Sentiment'][i] == 'Negative'):
            print(str(j) + ')' + NegativeDF ['Tweets'][i])
        print()
        j = j+i
        
    #Print Neutral tweets 

    j= 1
    NeutralDF = df.sort_values(by=['Polarity'])
    for i in range(0, NeutralDF.shape[0]):
        if(NeutralDF['Sentiment'][i] == 'Neutral'):
            print(str(j) + ')' + NeutralDF['Tweets'][i])
        print()
        j = j+i
    return df.T.to_dict()


    



def spotify_analysis(genre):
    import spotipy
    from spotipy.oauth2 import SpotifyClientCredentials
    import pandas as pd

    file_path= "/Users/prajesh/Desktop/Class_Activity/Project4/config.json"
    with open(file_path) as fp:
        config = json.loads(fp.read())
        
        
    #Authentication - without user
    
    client_credentials_manager = SpotifyClientCredentials(CLIENT_ID= (config['CLIENT_ID']), CLIENT_SECRET=(config['CLIENT_SECRET']))
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

    playlist_link = "https://open.spotify.com/playlist/37i9dQZEVXbNG2KDcFcKOF?si=1333723a6eff4b7f"
    playlist_URI = playlist_link.split("/")[-1].split("?")[0]
    track_uris = [x["track"]["uri"] for x in sp.playlist_tracks(playlist_URI)["items"]]

    artist_names = []
    track_names = []
    albums = []
    artist_pops = []
    artist_genres = []
    track_pops=[]

    artist_info = {}
    for track in sp.playlist_tracks(playlist_URI)["items"]:
        #URI
        track_uri = track["track"]["uri"]
        
        #Track name
        track_name = track["track"]["name"]
        
        #Main Artist
        artist_uri = track["track"]["artists"][0]["uri"]
        artist_info = sp.artist(artist_uri)
        
        #Name, popularity, genre
        artist_name = track["track"]["artists"][0]["name"]
        artist_pop = artist_info["popularity"]
        artist_genre = artist_info["genres"]

        
        #Album
        album = track["track"]["album"]["name"]
        
        #Popularity of the track
        track_pop = track["track"]["popularity"]

        #Description
        #description = track[""]

        track_names.append(track_name)
        artist_names.append(artist_name)
        artist_genres.append(artist_genre)
        artist_pops.append(artist_pop)
        track_pops.append(track_pop)

    df = {'artist':artist_names, 'track':track_names, 'genre':artist_genres, 'popularity':track_pops}
    pd.DataFrame(df)

    df1 = pd.DataFrame.from_dict(df)
    df1

    df2=df1.explode('genre')

    from musixmatch import Musixmatch
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

    # Musixmatch API
    musixmatch = (config['MUSIX_API'])

    analyser = SentimentIntensityAnalyzer()

    sentiment_list = []
    sentiment_score_list = []

    for i in df2[['track', 'artist']].values:
        try:
            song = musixmatch.matcher_lyrics_get(i[1], i[0])
            song = song['message']['body']['lyrics']['lyrics_body']
            sentiment_score = analyser.polarity_scores(song)

            if sentiment_score['compound'] >= 0.05:
                sentiment_percentage = sentiment_score['compound']
                sentiment = 'Positive'
            elif sentiment_score['compound'] > -0.05 and sentiment_score['compound'] < 0.05:
                sentiment_percentage = sentiment_score['compound']
                sentiment = 'Neutral'
            elif sentiment_score['compound'] <= -0.05:
                sentiment_percentage = sentiment_score['compound']
                sentiment = 'Negative'

            sentiment_list.append(sentiment)
            sentiment_score_list.append((abs(sentiment_percentage) * 100))
            
        except:
            sentiment_list.append('None')
            sentiment_score_list.append(0)

    df2['Sentiment'] = sentiment_list
    df2['Sentiment_Score'] = sentiment_score_list

    df2

    df2[df2['genre'].str.contains('pop',na=False)]

    df2[df2['genre'].str.contains('rock',na=False)]