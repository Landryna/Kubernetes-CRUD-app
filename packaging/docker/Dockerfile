FROM alpine:3.7

RUN apk add --no-cache python3 py3-pip

RUN pip3 install Werkzeug==0.16.1 \
     flask flask-restplus \
     requests kubernetes --upgrade pip

WORKDIR /src

COPY docker/src/ .

ENV FLASK_APP=main.py \
	K8S_ENVIRONMENT=False

RUN chown -R 65534 /src 

USER 65534

ENTRYPOINT ["flask","run"]
CMD ["--host","0.0.0.0"]
