FROM python:3
ENV PYTHONUNBUFFERED=1

WORKDIR /code

RUN apt-get update \
  && apt-get -y install netcat gcc postgresql \
  && apt-get clean

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /code/
