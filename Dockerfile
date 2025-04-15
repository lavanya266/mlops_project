FROM python:3.12

WORKDIR /flask_app

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

COPY tests/ app/tests/

CMD mlflow server --host 0.0.0.0 --port 5000 & \
    python app.py
