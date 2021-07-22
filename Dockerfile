FROM python:3.9.6-slim-buster

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev postgresql-client \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

RUN mkdir /code
WORKDIR /code

# run before copying code to make build on codechange faster
ADD requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /code

CMD ["scripts/run.sh"]
