FROM python:3.10-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1

WORKDIR /code
RUN apt-get -y update && apt-get -y install build-essential
COPY ./requirements.txt /code/
RUN     pip install --upgrade pip setuptools wheel \
        && pip install -r requirements.txt \
        && rm -rf /root/.cache/pip

COPY src/ /code/
EXPOSE 8000
CMD ["uvicorn", "main:app", "--reload", "--workers=1", "--host=0.0.0.0", "--port=8000"]
