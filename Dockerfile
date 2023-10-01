FROM tiangolo/uwsgi-nginx:python3.11

ENV NGINX_MAX_UPLOAD 16m
ENV LISTEN_PORT 8000
ENV UWSGI_CHEAPER 4
ENV UWSGI_PROCESSES 32
ENV NGINX_WORKER_PROCESSES 2
ENV UWSGI_INI /app/uwsgi.ini

RUN apt update
RUN apt install gettext
COPY custom-nginx.conf /etc/nginx/conf.d/custom.conf
WORKDIR /app


# Installing all python dependencies
ADD requirements.txt /app/
ADD requirements /app/requirements
RUN pip install -r requirements.txt

ADD prestart.sh /app/prestart.sh
ADD uwsgi.ini /app/uwsgi.ini
COPY . /app/