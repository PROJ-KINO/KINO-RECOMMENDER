import os

# 1. 동기화
os.system("python etl/sync_mysql_to_mongo.py")
# 2. 모델 학습
os.system("python -m recommender.svd_train")
# 3. 모델 평가
os.system("python etl/evaluate_svd.py")