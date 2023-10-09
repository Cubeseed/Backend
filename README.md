## Overview

This repository contains the Backend API endpoint for CubeSeed

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

## Run Test

```bash
    python manage.py test
```

## How To Use Docker

If you have docker installed and know how to run it from the command line:

```bash
docker run -it -dp 8000:8000 sebastiangh/cubeseed
```

### Install docker
 - [Windows](https://docs.docker.com/desktop/install/windows-install/)
 - [Mac](https://docs.docker.com/desktop/install/mac-install/)
 - [Ubuntu](https://docs.docker.com/engine/install/ubuntu/)

### How to build and push

```bash
  docker build -t cubeseed . -f docker/Dockerfile
  # tag not necessary if already done before
  docker tag cubeseed sebastiangh/cubeseed
  docker push sebastiangh/cubeseed
```

### Run project container

```bash
    docker-compose up
```

## Contributing
All new features, enhancements, bug fixes must be added as an issue before opening a PR.