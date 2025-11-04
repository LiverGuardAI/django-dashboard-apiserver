# React-project/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# 시스템 필수 패키지 설치 (mysqlclient 등 빌드 의존성 대비)
RUN apt-get update && apt-get install -y \
    build-essential \
    libmariadb-dev-compat \
    libmariadb-dev \
    && rm -rf /var/lib/apt/lists/*

# 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 프로젝트 복사
COPY . .

# collectstatic은 필요 시 docker-compose 단계에서 실행
CMD ["gunicorn", "reactproject.wsgi:application", "--bind", "0.0.0.0:8000"]