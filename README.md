## Overview

This repository contains the Backend endpoint for CubeSeed

## Requirements

You need the following tools to set up the project:
- Django
- Django Rest Framework
- Python

## Set up locally

1. Open Command Prompt on your local computer.

2. Clone the repository by clicking on `Code` option on top left of the main repository.

```bash
    git clone https://github.com/Cubeseed/Backend.git
```

3. Navigate to the project directory.

```bash
    cd Backend
```

4. Set up and Activate your virtual environment

```bash
    python3 -m venv env
    source env/bin/activate - # For Mac/Linux
    env\Scripts\activate - # For Windows
```

5. Install all project dependencies. 

```bash
    pip install -r requirements.txt
```

6. Migrate database

```bash
    python manage.py migrate
```

7. Run the project server locally.

```bash
    python manage.py runserver
```

8. Access the live development server at [localhost:8000/swagger](http://localhost:8000/swagger/).

## How To Use Docker

If you have docker installed and know how to run it from the command line:

```bash
docker run -it -dp 8000:8000 sebastiangh/cubeseed
```

### Install docker
 - [Windows](https://docs.docker.com/desktop/install/windows-install/)
 - [Mac](https://docs.docker.com/desktop/install/mac-install/)
 - [Ubuntu](https://docs.docker.com/engine/install/ubuntu/)

[Guide on how to run docker images](https://docs.docker.com/get-started/run-docker-hub-images/)

### Run project container
Look for the =sebastiangh/cubeseed= image: [[https://hub.docker.com/r/sebastiangh/cubeseed]]
Run with the following settings:
 - Name: Any name
 - Host Port: =8000=
 - Container Port: =8000=

### Run the database container (not needed for development)
Look for the postgres image: https://hub.docker.com/_/postgres.
Run with the following settings:
 - Name: whatever
 - Host Port: =5432=
 - Container Port: =5432=
 - Environment:
   + POSTGRES_PASSWORD=cubeseedsecret=
   + POSTGRES_USER=cubeseed=
   + POSTGRES_DB=cubeseedapi=

### How to build and push
```bash
  docker build -t cubeseed . -f docker/Dockerfile
  # tag not necessary if already done before
  docker tag cubeseed sebastiangh/cubeseed
  docker push sebastiangh/cubeseed
```

## Contributing
All new features, enhancements, bug fixes must be added as an issue before opening a PR.