from flask import Flask, request, jsonify

from recommender.data_loader import get_dataframes
from recommender.hybrid import hybrid_recommend

app = Flask(__name__)

@app.route('/recommend', methods=['POST'])
def recommend():
    user_id = int(request.json['user_id'])
    n = int(request.json.get('n', 20))
    movie_ids = hybrid_recommend(user_id, n_total=n)

    # short_review, my_pick_movie, movie_genre, user_genre, movies = get_dataframes()
    # print("short_review columns:", short_review.columns)
    # print(short_review.head())

    # MongoDB에서 영화 정보 가져오기
    movies, *_ = get_dataframes()
    # 추천 영화ID만 필터
    movie_info = movies[movies['movie_id'].isin(movie_ids)][['movie_id', 'title', 'still_cut_url']]
    # 추천된 순서대로 정렬
    movie_info['order'] = movie_info['movie_id'].apply(lambda x: movie_ids.index(x))
    movie_info = movie_info.sort_values('order')

    # 딕셔너리 리스트로 반환
    result = movie_info[['movie_id', 'title', 'still_cut_url']].to_dict(orient='records')
    return jsonify({'movies': result})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)