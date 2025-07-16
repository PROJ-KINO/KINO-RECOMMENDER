from recommender.data_loader import get_dataframes
from surprise import SVD, Dataset, Reader
from surprise.model_selection import cross_validate
import pandas as pd

def evaluate_svd():
    _, _, _, short_review, my_pick_movie = get_dataframes()
    pick_df = my_pick_movie.copy()
    pick_df['rating'] = 5
    pick_df = pick_df[['user_id', 'movie_id', 'rating']]
    ratings = pd.concat([short_review[['user_id','movie_id','rating']], pick_df])

    reader = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_df(ratings, reader)
    algo = SVD()
    results = cross_validate(algo, data, measures=['RMSE', 'MAE'], cv=3, verbose=True)
    print('평균 RMSE:', results['test_rmse'].mean())
    print('평균 MAE:', results['test_mae'].mean())

if __name__ == "__main__":
    evaluate_svd()