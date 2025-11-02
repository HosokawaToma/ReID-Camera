FROM python:3.10.17

RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["python", "src/main.py"]
