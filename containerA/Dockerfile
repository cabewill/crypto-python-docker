ARG PYTHON_VERSION=3.8.1-slim

FROM python:${PYTHON_VERSION} as build

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt /etc

RUN pip install -r /etc/requirements.txt 

WORKDIR /app
COPY . /app


FROM python:${PYTHON_VERSION} as prod
COPY --from=build /opt/venv /opt/venv
WORKDIR /app
RUN mkdir /data && mkdir /key
COPY /src /app
ENV PATH="/opt/venv/bin:$PATH"
# CMD ["sh"]
CMD ["python3", "monitor.py"]