# 初期セットアップ

## Docker のインストール

```
# 必要なパッケージをインストール
sudo apt update
sudo apt install ca-certificates curl gnupg lsb-release
# Docker の公式 GPG キーを取得
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
# Docker リポジトリの登録
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
# Docker のインストール
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin
# 現在のユーザを Docker グループに追加
sudo usermod -aG docker $USER
```

## .env ファイルの作成


## 起動
