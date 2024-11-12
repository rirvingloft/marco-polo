FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt /app/
COPY app.py /app/
RUN apt-get update && apt-get install -y curl wget
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "app.py"]
