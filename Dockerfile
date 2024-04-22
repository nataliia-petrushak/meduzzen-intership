FROM python:3.12.0-alpine

WORKDIR /code

COPY ./requirements.txt .

RUN apk add --no-cache build-base libffi-dev openssl-dev

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

CMD ["python", "app/main.py"]
