FROM python:3.7

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY assets assets/
COPY *.py index.html ./
COPY data/ ./data
COPY assets/ ./assets
ENTRYPOINT python app.py
