FROM python:3.10.17

WORKDIR /app

ENV OMP_NUM_THREADS=1
ENV MKL_NUM_THREADS=1

RUN mkdir -p /app/config && chmod -R 777 /app/config
ENV YOLO_CONFIG_DIR=/app/config

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ./src ./src
COPY ./resources ./resources

ENTRYPOINT ["python", "src/main.py"]
