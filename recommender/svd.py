from surprise import SVD, Dataset, Reader
import pandas as pd
import pickle
import datetime
import os

def train_svd(short_review_df, my_pick_movie_df):
    # my_pick_movie: 찜한 영화는 rating=5로 간주
    pick_df = my_pick_movie_df.copy()
    pick_df['rating'] = 5
    pick_df = pick_df[['user_id', 'movie_id', 'rating']]
    ratings = pd.concat([short_review_df[['user_id','movie_id','rating']], pick_df])

    reader = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_df(ratings, reader)
    trainset = data.build_full_trainset()

    algo = SVD()
    algo.fit(trainset)

    # 1. 타임스탬프 파일명
    now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    model_dir = 'recommender/model'
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
    model_path = f'{model_dir}/svd_model_{now}.pkl'
    with open(model_path, 'wb') as f:
        pickle.dump(algo, f)

    # 2. 최신 모델 파일명을 last_model.txt에 저장
    with open(f'{model_dir}/last_model.txt', 'w') as f:
        f.write(model_path)

    print(f"SVD 모델 학습 및 저장 완료! 모델 파일: {model_path}")