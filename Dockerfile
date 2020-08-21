FROM python:3.8.5

WORKDIR /app

ENV FLASK_APP main.py
ENV FLASK_RUN_HOST 0.0.0.0

ADD . /app

RUN pip install -r requirements.txt

EXPOSE 5000
CMD ["flask", "run"]

