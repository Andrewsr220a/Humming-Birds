#Import the Libraries 
from textblob import TextBlob, Word, Blobber
from wordcloud import WordCloud 
import tweepy
import pandas as pd
import numpy as np 
import re
import matplotlib.pyplot as plt
import json
from flask import Flask, render_template, redirect, jsonify

def twitter_sentiments(twitter_handle):

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
    post = api.user_timeline(screen_name= "twitter_handle", count = 100, lang= "en", tweet_mode = "extended")

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
    df

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
    df

    # Visualizing using the WordCloud
    all_words = " ".join( [twts for twts in df['Tweets']])
    wordCloud = WordCloud(width = 600, height = 400, random_state = 20, max_font_size = 120 ).generate(all_words)

    plt.imshow(wordCloud, interpolation= "bilinear")
    plt.axis("off")
    plt.show()

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
    df

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
