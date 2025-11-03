FROM python:3.10.17

WORKDIR /app

RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app/config && chmod -R 777 /app/config
ENV YOLO_CONFIG_DIR=/app/config

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ./src ./src
COPY ./resources ./resources

ENTRYPOINT ["python", "src/main.py"]
