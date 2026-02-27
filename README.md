# ReID-Camera

カメラから取得したフレームを API に送信し続けるアプリケーション。

## 必要な環境

- Python 3.x
- カメラ（Webカメラまたはビデオキャプチャデバイス）

## セットアップ

### 1. .env ファイルの作成

プロジェクトルートに `.env` ファイルを作成し、以下の環境変数を設定してください。

```bash
cp .env.example .env
```

### 2. セットアップスクリプトを実行

```bash
sh setup.sh
```

## プロジェクト構成

```
ReID-Camera/
├── src/
│   ├── main.py                 # エントリポイント
│   ├── application/            # アプリケーション層（カメラ・スナップショット送信）
│   ├── domain/                 # ドメイン層（フレーム等）
│   ├── dto/                    # データ転送オブジェクト
│   ├── repository/             # リポジトリ層（API 通信・トークン取得）
│   ├── environment.py          # 環境変数
│   ├── error.py
│   └── logger.py
├── requirements.txt
└── README.md
```
