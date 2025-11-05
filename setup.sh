#!/bin/bash

set -e  # エラーが発生したらスクリプトを停止

# 色の定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== ReID-Camera セットアップスクリプト ===${NC}"

# プロジェクトのルートディレクトリを取得
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_NAME="ReID-Camera"
VENV_PATH="$PROJECT_ROOT/.venv"
SERVICE_FILE="$PROJECT_ROOT/ReID-Camera.service"
SYSTEMD_SERVICE_PATH="/etc/systemd/system/ReID-Camera.service"

# Python のインストール確認
echo -e "${YELLOW}[1/5] Python のインストール確認中...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}Python3 が見つかりません。インストールします...${NC}"

    # OS の判定
    if [ -f /etc/debian_version ]; then
        # Debian/Ubuntu
        sudo apt update
        sudo apt install -y python3 python3-pip python3-venv
    elif [ -f /etc/redhat-release ]; then
        # RHEL/CentOS/Fedora
        sudo yum install -y python3 python3-pip
        sudo yum install -y python3-venv || sudo yum install -y python3-virtualenv
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if ! command -v brew &> /dev/null; then
            echo -e "${RED}Homebrew がインストールされていません。先に Homebrew をインストールしてください。${NC}"
            exit 1
        fi
        brew install python3
    else
        echo -e "${RED}サポートされていないOSです。手動でPython3をインストールしてください。${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}Python3 は既にインストールされています。${NC}"
fi

# Python バージョンの確認
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo -e "${GREEN}Python バージョン: $PYTHON_VERSION${NC}"

# 仮想環境の作成
echo -e "${YELLOW}[2/5] 仮想環境の作成中...${NC}"
if [ ! -d "$VENV_PATH" ]; then
    python3 -m venv "$VENV_PATH"
    echo -e "${GREEN}仮想環境を作成しました: $VENV_PATH${NC}"
else
    echo -e "${GREEN}仮想環境は既に存在します。${NC}"
fi

# 仮想環境の有効化と依存関係のインストール
echo -e "${YELLOW}[3/5] 依存関係のインストール中...${NC}"
source "$VENV_PATH/bin/activate"
pip install --upgrade pip
pip install -r "$PROJECT_ROOT/requirements.txt"
echo -e "${GREEN}依存関係のインストールが完了しました。${NC}"

# サービスファイルの設定
echo -e "${YELLOW}[4/5] サービスファイルの設定中...${NC}"

# サービスファイルのパスを更新（macOSとLinuxの両方に対応）
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    sed -i '' "s|WorkingDirectory=.*|WorkingDirectory=$PROJECT_ROOT/src|g" "$SERVICE_FILE"
    sed -i '' "s|ExecStart=.*|ExecStart=$VENV_PATH/bin/python $PROJECT_ROOT/src/main.py|g" "$SERVICE_FILE"
else
    # Linux
    sed -i "s|WorkingDirectory=.*|WorkingDirectory=$PROJECT_ROOT/src|g" "$SERVICE_FILE"
    sed -i "s|ExecStart=.*|ExecStart=$VENV_PATH/bin/python $PROJECT_ROOT/src/main.py|g" "$SERVICE_FILE"
fi

# systemd サービスファイルのコピー
if [ "$EUID" -ne 0 ]; then
    echo -e "${YELLOW}systemd サービスファイルをコピーするために sudo 権限が必要です。${NC}"
    sudo cp "$SERVICE_FILE" "$SYSTEMD_SERVICE_PATH"
    sudo chmod 644 "$SYSTEMD_SERVICE_PATH"
else
    cp "$SERVICE_FILE" "$SYSTEMD_SERVICE_PATH"
    chmod 644 "$SYSTEMD_SERVICE_PATH"
fi

echo -e "${GREEN}サービスファイルを設定しました: $SYSTEMD_SERVICE_PATH${NC}"

# systemd のリロードとサービスの有効化・起動
echo -e "${YELLOW}[5/5] サービスの起動中...${NC}"

if [ "$EUID" -ne 0 ]; then
    sudo systemctl daemon-reload
    sudo systemctl enable ReID-Camera.service
    sudo systemctl start ReID-Camera.service
else
    systemctl daemon-reload
    systemctl enable ReID-Camera.service
    systemctl start ReID-Camera.service
fi

# サービス状態の確認
echo -e "${GREEN}サービス状態を確認中...${NC}"
if [ "$EUID" -ne 0 ]; then
    sudo systemctl status ReID-Camera.service --no-pager -l
else
    systemctl status ReID-Camera.service --no-pager -l
fi

echo -e "${GREEN}=== セットアップが完了しました！ ===${NC}"
echo -e "${GREEN}サービスを管理するコマンド:${NC}"
echo -e "  起動: sudo systemctl start ReID-Camera"
echo -e "  停止: sudo systemctl stop ReID-Camera"
echo -e "  再起動: sudo systemctl restart ReID-Camera"
echo -e "  状態確認: sudo systemctl status ReID-Camera"
echo -e "  ログ確認: sudo journalctl -u ReID-Camera -f"

