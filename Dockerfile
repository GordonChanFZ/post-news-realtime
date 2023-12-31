FROM python:3.10-slim-bullseye

LABEL maintainer="gordonchanfz@ai-note.xyz"
ARG TZ='Asia/Shanghai'

WORKDIR /app

COPY . .

RUN /usr/local/bin/python -m pip install --no-cache --upgrade pip \
    && pip install --no-cache -r requirements.txt



RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
