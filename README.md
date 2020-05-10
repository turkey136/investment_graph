### システム構成
- docker 19.03.8
- docker-comporse 1.25.5

### コンテナ構築
```bash
docker-comporse up -d
```

### DB 作成
```bash
# コンテナ内で処理しない場合、docker run あたりで代替してください
docker-comporse exec server bash

# table 作成
cd src
python migrate.py

# 既存データ作成
python seed.py
```