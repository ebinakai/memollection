# memollection

Flaskで初めて作ったWebアプリケーション。チャット形式でメモが書ける。一人Twitter的なイメージで作った。けど、明らかにLINE。

## セットアップ

1. 仮想環境の作成
2. 仮想環境の有効化
3. パッケージのインストール
4. Flaskアプリケーションのパスを設定
5. データベースの初期化

```[bash]
python -m venv env
source ./env/bin/activate
pip install -r requirements.txt
export FLASK_APP=app.py
flask init-db
```

### データベースに繋がらない場合

```[bash]
sudo apt-get update
sudo apt-get install sqlite3 libsqlite3-dev
sqlite3

sqlite> .open --new memollection.db
sqlite> .exit
```

## 実行
```[bash]
python app.py
```
