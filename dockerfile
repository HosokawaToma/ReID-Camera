# pip install
FROM python:3.10.17 AS pip-install
COPY requirements.txt .
RUN pip install -r requirements.txt

# メイン
FROM python:3.10.17

WORKDIR /app

RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

COPY --from=pip-install /usr/local /usr/local

COPY ./src ./src
COPY ./resources ./resources

ENTRYPOINT ["python", "src/main.py"]
