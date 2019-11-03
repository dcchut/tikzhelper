FROM alpine:latest

EXPOSE 3031
VOLUME /usr/src/app/public
WORKDIR /usr/src/app

RUN apk add --no-cache uwsgi-python3 python3
RUN rm -rf public/*

# Install requirements to get the benefits of cacheing
COPY requirements.txt .
RUN python3 -m pip install --no-cache-dir -r requirements.txt

# Install for real
COPY . .
RUN python3 -m pip install --no-cache-dir -e .

CMD [ "uwsgi", "--socket", "0.0.0.0:3031", \
               "--plugins", "python3", \
               "--paste", "config:/usr/src/app/production.ini", \
               "--uid", "uwsgi" ]
