# Server Docker File - Python based using flask
FROM python:3.8

RUN mkdir /app
WORKDIR /app
ADD . /app

RUN pip3 install -r requirements.txt

ENTRYPOINT [ "python3" ]

CMD ["app.py" ]