FROM python:3.12.0-alpine

WORKDIR /code

COPY ./requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

RUN pip install .

CMD ["python", "app/main.py"]
