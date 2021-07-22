FROM python:3.9.6

RUN apt-get update \
  # dependencies for building Python packages and psycopg2
  && apt-get install -y build-essential libpq-dev postgresql-client

RUN mkdir /code
WORKDIR /code

# run before copying code to make build on codechange faster
ADD requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /code

CMD ["./run.sh"]
