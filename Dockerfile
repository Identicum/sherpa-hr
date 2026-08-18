FROM ghcr.io/identicum/python-flask:latest

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./app/ /app

RUN apk add --no-cache postgresql-client
COPY ./db/ /db/
COPY init_db.sh /init_db.sh
RUN chmod +x /init_db.sh
