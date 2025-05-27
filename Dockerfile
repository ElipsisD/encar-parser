FROM python:3.12.9

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN pip install requests

WORKDIR /app

COPY ./app /app


CMD ["python", "app.py"]
