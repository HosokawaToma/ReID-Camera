# pip install
FROM python:3.10.17 AS pip-install
COPY requirements.txt .
RUN pip install -r requirements.txt

# apt install
FROM python:3.10.17 AS apt-install
RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

# メイン
FROM python:3.10.17

WORKDIR /app

COPY --from=apt-install /usr/local /usr/local

COPY --from=pip-install /usr/local /usr/local

COPY . .

ENTRYPOINT ["python", "src/main.py"]
