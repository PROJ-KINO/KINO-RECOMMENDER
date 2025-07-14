from pymongo import MongoClient
import pandas as pd

def get_dataframes():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['kino']
    movies = pd.DataFrame(list(db['movies'].find()))
    user_genre = pd.DataFrame(list(db['user_genre'].find()))
    movie_genre = pd.DataFrame(list(db['movie_genre'].find()))
    short_review = pd.DataFrame(list(db['short_review'].find()))
    my_pick_movie = pd.DataFrame(list(db['my_pick_movie'].find()))
    client.close()
    return movies, user_genre, movie_genre, short_review, my_pick_movie