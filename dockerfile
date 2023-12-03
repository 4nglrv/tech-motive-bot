FROM python:3.11.6-slim-bullseye

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

ENV PYTHONPATH=/app

COPY ./app /app

CMD ["python", "app/main.py"]