import pymysql
from pymongo import MongoClient
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DB = os.getenv('MYSQL_DB')
MONGO_URI = os.getenv('MONGO_URI')

# 1. MySQL 연결
mysql_conn = pymysql.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    db=MYSQL_DB,
    charset='utf8'
)

# 2. MongoDB 연결
mongo_client = MongoClient(MONGO_URI)
mongo_db = mongo_client['kino']

def table_to_mongo(sql, mongo_collection):
    df = pd.read_sql(sql, mysql_conn)
    # 1. 날짜 컬럼
    if 'release_date' in df.columns:
        df['release_date'] = df['release_date'].apply(
            lambda x: x.strftime('%Y-%m-%d') if not pd.isnull(x) else None
        )
    # created_at
    if 'created_at' in df.columns and df['created_at'].dtype == 'object':
        df['created_at'] = df['created_at'].astype(str)
    # 2. bool/bytes → bool/int 변환
    if 'is_deleted' in df.columns:
        df['is_deleted'] = df['is_deleted'].apply(lambda x: bool(x) if type(x) is not bool else x)
    # 3. None/NaN → None
    df = df.where(pd.notnull(df), None)

    # 4. Mongo에 insert
    mongo_collection.delete_many({})  # 전체 삭제 후
    if not df.empty:
        mongo_collection.insert_many(df.to_dict('records'))
    print(f"{mongo_collection.name} 동기화 완료: {len(df)}건")

# 3. 각 테이블 동기화
table_to_mongo('SELECT * FROM movie', mongo_db['movies'])
table_to_mongo('SELECT * FROM user_genre', mongo_db['user_genre'])
table_to_mongo('SELECT * FROM movie_genre', mongo_db['movie_genre'])
table_to_mongo('SELECT user_id, movie_id, rating FROM short_review', mongo_db['short_review'])
table_to_mongo('SELECT * FROM my_pick_movie', mongo_db['my_pick_movie'])

mysql_conn.close()
mongo_client.close()