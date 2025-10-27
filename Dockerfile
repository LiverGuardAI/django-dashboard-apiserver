# --- Base Image (Python + Linux)
FROM python:3.11-slim

# --- Work Directory
WORKDIR /app

# --- Install Python Dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# --- Copy Django Project
COPY . .

# --- PyMySQL 활성화 (settings.py에서 필요)
# CMD에서 자동 주입할 수도 있지만, 보통 settings.py에 아래 2줄 추가:
# import pymysql
# pymysql.install_as_MySQLdb()

# --- Run Django Dev Server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

