from surprise import SVD, Dataset, Reader
import pandas as pd
import pickle

def train_svd(short_review_df, my_pick_movie_df):
    # my_pick_movie: 찜한 영화는 rating=5로 간주(예시)
    pick_df = my_pick_movie_df.copy()
    pick_df['rating'] = 5
    pick_df = pick_df[['user_id', 'movie_id', 'rating']]
    ratings = pd.concat([short_review_df[['user_id','movie_id','rating']], pick_df])

    reader = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_df(ratings, reader)
    trainset = data.build_full_trainset()

    algo = SVD()
    algo.fit(trainset)
    with open('recommender/model/svd_model.pkl', 'wb') as f:
        pickle.dump(algo, f)
    print("SVD 모델 학습 및 저장 완료!")