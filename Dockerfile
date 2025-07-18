FROM python:3.10

# 컨테이너 작업 폴더 지정
WORKDIR /app

# requirements.txt 복사 및 패키지 설치
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 프로젝트 소스 전체 복사
COPY . .

# Flask 서버 포트
EXPOSE 5001

# Flask 실행 명령
CMD ["python", "app.py"]