# syntax=docker/dockerfile:1

FROM python:3

#ARG BUILD_BRANCH=main
ARG VERSION=v0.0.0.0.0.0
ARG DJANGO_SETTINGS_MODULE=cubeseed.settings
ENV VERSION=${VERSION}
ENV DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE}

LABEL org.opencontainers.image.source=https://github.com/Cubeseed/Backend
LABEL org.opencontainers.image.description="Cubeseed API"
LABEL org.opencontainers.image.licenses=FIXME
LABEL org.opencontainers.image.version=${VERSION}

WORKDIR /app
#RUN git clone -b ${BUILD_BRANCH} https://github.com/Cubeseed/Backend.git /app
COPY . /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENTRYPOINT ["python3"]

EXPOSE 8000
