ARG PYTHON_VERSION=3.8.1-slim

FROM python:${PYTHON_VERSION} as build

RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    libpq-dev \
    gcc \
  && rm -rf /var/lib/apt/lists/* \
  && pip3 install --upgrade pip

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app

COPY requirements.txt /etc

RUN pip install -r /etc/requirements.txt 

COPY . /app

FROM python:${PYTHON_VERSION} as prod
COPY --from=build /opt/venv /opt/venv
WORKDIR /app
RUN mkdir /data && mkdir /key
COPY /src /app
ENV PATH="/opt/venv/bin:$PATH"

CMD ["uwsgi", "--ini", "/app/wsgi.ini"]
