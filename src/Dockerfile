FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

COPY ./requirements.txt ./
RUN apt-get update
RUN apt-get install libportaudio2 -y
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir --no-deps -r requirements.txt

# chown to non-root user then copy all files in source dir to dest
COPY --chown=1000:1000 . .
# CMD [ "python3", "./backend/manage.py", "runserver" ]