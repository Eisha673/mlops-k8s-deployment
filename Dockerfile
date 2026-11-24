FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir --default-timeout=1000 --retries 10 mlflow-skinny scikit-learn flask gunicorn
RUN pip install --no-cache-dir --default-timeout=1000 --retries 10 pandas
RUN pip install --no-cache-dir --default-timeout=1000 --retries 10 skops uvicorn
COPY mlruns/1/models/m-c1d27f9beefa477e944ce11ed841171a/artifacts /app/model
EXPOSE 8080
CMD ["mlflow", "models", "serve", "-m", "/app/model", "--host", "0.0.0.0", "--port", "8080", "--env-manager", "local"]
