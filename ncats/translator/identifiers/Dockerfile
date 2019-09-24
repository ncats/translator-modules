FROM python:3

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY server /home/server

WORKDIR /home

ENTRYPOINT ["python3", "-m", "server"]
