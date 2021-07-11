FROM ubuntu:latest as build
RUN apt update && apt install -y gfortran && apt clean
ADD ./*.f08 /src/
WORKDIR /src 
RUN gfortran hello.f08 -o hello

FROM ubuntu:latest
ENV DEBIAN_FRONTEND "noninteractive"
RUN apt update && apt install -y python3 python3-pip uwsgi-plugin-python3 nginx uwsgi libgfortran5 curl supervisor && apt clean
WORKDIR /app
ADD ./*.py /app/
ADD ./requirements.txt /app/
RUN pip3 install -r requirements.txt
ADD ./flask.conf /etc/nginx/conf.d/
ADD ./uwsgi.ini /app/
ADD ./supervisord.conf /etc/supervisor/conf.d/supervisord.conf
EXPOSE 8000
COPY --from=build /src/hello /app/
#CMD python3 /app/app.py
CMD ["/usr/bin/supervisord", "-n"]