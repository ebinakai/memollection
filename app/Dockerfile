# ベースイメージとしてPython 3.9を使用する
FROM python:3.9

# 作業ディレクトリを設定する
WORKDIR /

# 必要なライブラリの依存関係をコピーし、インストールする
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app
# ソースコードをコンテナにコピーする
COPY . .

# コンテナ起動時にFlaskアプリケーションを実行する
CMD ["python", "/app/app.py"]
