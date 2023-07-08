# syntax=docker/dockerfile:1
FROM python:3
WORKDIR /app
ARG BUILD_BRANCH=main
ARG ALLOWED_HOSTS=localhost
RUN git clone -b ${BUILD_BRANCH} https://github.com/Cubeseed/Backend.git /app
RUN sed -i "s/ALLOWED_HOSTS = \[.*\]/ALLOWED_HOSTS = \['${ALLOWED_HOSTS}'\]/g" cubeseed/settings.py
RUN cat cubeseed/settings.py
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python3 manage.py migrate

ENTRYPOINT ["python3"]
CMD ["manage.py", "runserver", "0.0.0.0:8000"]

EXPOSE 8000
