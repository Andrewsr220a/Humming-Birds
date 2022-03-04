# Import dependecies
from utils import create_dataframe, print_name, process_sum, process_number_2, call_spotify_db, call_twitter_db
from flask import Flask, jsonify, render_template
from flask import Flask, render_template, redirect, jsonify
import pandas as pd
from sqlalchemy import create_engine, func
import json

# file_path = "/Users/raishandrews/Documents/GitHub/Humming-Birds/config.json"
# with open(file_path) as fp:
#     config = json.loads(fp.read())

connection_string = "postgres:Dontforget123!@localhost:5432/twitter_sentiments"
# engine = create_engine(f'postgresql://{connection_string}')
# app = Flask(__name__)
