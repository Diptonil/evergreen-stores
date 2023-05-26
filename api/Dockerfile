FROM python:3.10.11-alpine3.18

WORKDIR /app

ENV ADDRESS=

COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .

CMD [ "python3", "api.py"]