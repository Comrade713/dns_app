FROM python:3.9-slim

WORKDIR /app

COPY . /app

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 9090

CMD ["uvicorn", "FS:app", "--host", "0.0.0.0", "--port", "9090"]
