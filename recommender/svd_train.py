from recommender.data_loader import get_dataframes
from recommender.svd import train_svd

_, _, _, short_review, my_pick_movie = get_dataframes()
train_svd(short_review, my_pick_movie)
print("SVD 모델 학습 및 저장 완료!")