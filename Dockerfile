FROM python:3.11.7-alpine3.19

WORKDIR /usr/src/lbc-watchresell

RUN apk add gcc musl-dev linux-headers libc-dev
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "-u", "./main.py" ]