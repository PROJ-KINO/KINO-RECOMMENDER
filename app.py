from flask import Flask, request, jsonify

from recommender.data_loader import get_dataframes
from recommender.hybrid import hybrid_recommend

app = Flask(__name__)

@app.route('/recommend', methods=['POST'])
def recommend():
    user_id = int(request.json['user_id'])
    n = int(request.json.get('n', 20))
    movie_ids = hybrid_recommend(user_id, n_total=n)

    # 데이터 불러오기
    movies, _, movie_genre, genres, *_ = get_dataframes()

    # 추천 영화만 필터링
    movie_info = movies[
        (movies['movie_id'].isin(movie_ids)) &
        (movies['still_cut_url'].notnull()) &
        (movies['still_cut_url'] != '')
    ][['movie_id', 'title', 'still_cut_url', 'poster_url', 'plot', 'release_date', 'running_time', 'age_rating']].copy()

    movie_info['order'] = movie_info['movie_id'].apply(lambda x: movie_ids.index(x))
    movie_info = movie_info.sort_values('order')

    # 영화 ID별로 장르 이름 리스트 매핑
    # movie_genre: movie_id, genre_id
    # genres: genre_id, genre_name
    genre_map = genres.set_index('genre_id')['genre_name'].to_dict()
    movie_genre_group = movie_genre.groupby('movie_id')['genre_id'].apply(list)

    def genre_names(movie_id):
        ids = movie_genre_group.get(movie_id, [])
        unique_ids = set(ids)  # 중복 제거!
        return [genre_map.get(gid) for gid in unique_ids if gid in genre_map]

    movie_info['genres'] = movie_info['movie_id'].apply(genre_names)

    # JSON 반환
    result = movie_info[
        ['movie_id', 'title', 'still_cut_url', 'poster_url', 'plot', 'release_date', 'running_time', 'age_rating', 'genres']
    ].to_dict(orient='records')
    return jsonify({'movies': result})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)