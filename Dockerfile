FROM python:3.11-alpine

ADD ./app/requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt

COPY ./app /app/

EXPOSE 80

WORKDIR /app

CMD [ "flask", "run", "--host=0.0.0.0", "--port=80" ]
