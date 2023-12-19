FROM python:3.10

LABEL maintainer="gordonchanfz@ai-note.xyz"
ARG TZ='Asia/Shanghai'

RUN && /usr/local/bin/python -m pip install --no-cache --upgrade pip \
    && pip install --no-cache -r requirements.txt \

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "main.py"]
