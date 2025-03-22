# memollection

https://github.com/EbinaKai/memollection/assets/85666313/94b0a4b5-5088-417e-88c1-05d15d1a5aee

---

Flaskで初めて作ったWebアプリケーション。チャット形式でメモが書ける。一人Twitter的なイメージで作った。けど、明らかにLINE。

## セットアップ

```bash
docker build ./app -t memollection/app:1.0.0
docker tag memollection/app:1.0.0 registry.kb/memollection/app:1.0.0

# 初回のみ
kubectl apply -f db-secret.yaml
kubectl apply -f mysql-pv.yaml
kubectl apply -f mysql-statefulset.yaml
kubectl apply -f app-deployment.yaml
```
