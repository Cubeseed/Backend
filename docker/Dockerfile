# syntax=docker/dockerfile:1
FROM python:3
WORKDIR /app
ARG BUILD_BRANCH=main
RUN git clone -b ${BUILD_BRANCH} https://github.com/Cubeseed/Backend.git /app
RUN git branch
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python3 manage.py migrate

ENTRYPOINT ["python3"]
CMD ["manage.py", "runserver", "0.0.0.0:8000"]

EXPOSE 8000
