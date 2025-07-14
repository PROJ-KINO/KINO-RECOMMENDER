def genre_based_recommend(user_id, movies, user_genre, movie_genre, seen_ids, top_n=5):
    # 1. 유저가 선택한 장르
    genres = user_genre[user_genre['user_id'] == user_id]['genre_id'].tolist()
    # 2. 해당 장르 영화 중 아직 안 본/안 찜한 영화만 추림
    candidate_ids = set(movie_genre[movie_genre['genre_id'].isin(genres)]['movie_id']) - set(seen_ids)
    # 3. 후보 영화 정보
    candidates = movies[movies['movie_id'].isin(candidate_ids)]
    # 4. total_view 기준 내림차순 정렬해서 top_n만 반환
    pick = candidates.sort_values('total_view', ascending=False)['movie_id'].head(top_n).tolist()
    return pick