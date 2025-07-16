import pickle
from recommender.data_loader import get_dataframes
from recommender.content import genre_based_recommend

def get_latest_model_path():
    with open('recommender/model/last_model.txt') as f:
        return f.read().strip()

def hybrid_recommend(user_id, n_total=20, n_cf=15, n_content=5):
    movies, user_genre, movie_genre, short_review, my_pick_movie = get_dataframes()
    seen = set(short_review[short_review['user_id']==user_id]['movie_id']).union(
           set(my_pick_movie[my_pick_movie['user_id']==user_id]['movie_id']))

    # 1. 협업필터링 추천
    model_path = get_latest_model_path()
    with open(model_path, 'rb') as f:
        algo = pickle.load(f)
    all_movie_ids = set(movies['movie_id']) - seen
    preds = [(mid, algo.predict(user_id, mid).est) for mid in all_movie_ids]
    cf_ids = [mid for mid, _ in sorted(preds, key=lambda x:x[1], reverse=True)[:n_cf]]

    # 2. 장르 취향 추천
    content_ids = genre_based_recommend(user_id, movies, user_genre, movie_genre, seen, top_n=n_content)

    # 3. 합치기 (중복 제거, cf 우선)
    result = []
    for mid in cf_ids + content_ids:
        if mid not in result:
            result.append(mid)
        if len(result) == n_total:
            break
    return result