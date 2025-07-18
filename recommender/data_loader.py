from pymongo import MongoClient
import pandas as pd
import os

def get_dataframes():
    mongo_uri = os.environ.get("MONGO_URI", "mongodb://mongo:27017/kino")
    client = MongoClient(mongo_uri)
    db = client['kino']
    movies = pd.DataFrame(list(db['movies'].find()))
    user_genre = pd.DataFrame(list(db['user_genre'].find()))
    movie_genre = pd.DataFrame(list(db['movie_genre'].find()))
    short_review = pd.DataFrame(list(db['short_review'].find()))
    my_pick_movie = pd.DataFrame(list(db['my_pick_movie'].find()))
    client.close()
    return movies, user_genre, movie_genre, short_review, my_pick_movie