FROM python:3.12

WORKDIR /flask_app

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

COPY tests/ app/tests/

CMD mlflow server --host 0.0.0.0 --port 8000 & \
    python app.py


# # Use Python base image
# FROM python:3.12

# # Set the working directory inside the container
# WORKDIR /flask_app

# # Copy requirements.txt and install dependencies
# COPY requirements.txt .

# RUN pip install --upgrade pip
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy the Flask app and tests
# COPY app/ .
# COPY tests/ app/tests/

# # Install MLflow
# RUN pip install mlflow

# # Expose both the Flask and MLflow ports
# EXPOSE 5000
# EXPOSE 5001

# # Command to run MLflow server and Flask app
# CMD mlflow server --host 0.0.0.0 --port 5000 & \
#     python app.py
