## Overview

This repository contains the Backend API endpoint for CubeSeed

## Technologies

You need the following tools to set up the project:
- Django
- Django Rest Framework
- Python3
- Celery
- Rabbitmq Server
- Docker (Optional)

 ## Why use Django?
- Django provides a robust and scalable architecture for building web applications, with built-in support for common web development tasks such as routing, templating, and authentication.
- Django includes a powerful Object-Relational Mapping (ORM) system that makes it easy to work with databases and data models, without having to write SQL code directly.
- Django provides a rich set of built-in features and modules, including an admin interface, form handling, and user authentication, which can help to speed up development and reduce the amount of boilerplate code that needs to be written.
- Django has a large and active community of users and contributors, which means that there is a wealth of documentation, tutorials, and support available for developers who are new to the platform.

## Why use a task worker?
- Task workers provide a way to offload long-running or resource-intensive tasks from the main application thread, which can improve overall application performance and responsiveness.
- Task workers can help to manage high volumes of work by allowing tasks to be processed asynchronously and in parallel, which can improve overall throughput and reduce processing times.
- Task workers can provide fault tolerance and reliability by allowing tasks to be retried or processed by different workers if one worker fails.
- Task workers can help to decouple different parts of a system, making it easier to modify or replace individual components without affecting the rest of the system.
- Compared to other techniques such as direct API calls or database polling, task workers can be more efficient and scalable, especially when dealing with large volumes of data or complex processing requirements.
- Task workers can be easily scaled horizontally by adding more worker instances, which can help to handle sudden spikes in workload or accommodate growing demand over time.
- Task workers can be used to implement a wide range of processing patterns, including batch processing, event-driven processing, and real-time processing, making them a versatile choice for many different types of applications.


## Why use Celery?
- Celery is a widely used and well-established task queue that has been around for over a decade, with a large and active community of users and contributors.
- Celery provides a flexible and powerful framework for defining and executing tasks, with support for a wide range of task types, including periodic tasks, retryable tasks, and subtasks.
- Celery supports a wide range of message brokers, including RabbitMQ, Redis, and Amazon SQS, making it a versatile choice for many different types of applications.
- Celery provides a rich set of features and capabilities, including task result storage, task prioritization, and task routing, as well as support for monitoring and management through tools like Flower and celerybeat.
- Celery is highly scalable and can handle large volumes of tasks and high levels of traffic, making it a good choice for applications with demanding performance requirements.
- Celery is open source and free to use, with a permissive license that allows for commercial use and modification.
- Compared to other task workers such as RQ or Dramatiq, Celery is generally considered to be more feature-rich and flexible, with a wider range of configuration options and a more mature ecosystem of plugins and integrations.

## Why use a message broker?
- Message brokers provide a way to manage the flow of messages between different parts of a system, which can improve overall system performance and scalability.
- Message brokers can be used to implement a wide range of processing patterns, including publish-subscribe, point-to-point, and request-response, making them a versatile choice for many different types of applications.

## Why use a message broker with Celery for Django task queues?
When using Celery for Django task queues, a message broker can be particularly useful for several reasons:
- Message brokers like RabbitMQ can help to manage the flow of messages between different parts of a system, allowing tasks to be distributed across multiple worker instances and ensuring that tasks are processed reliably and without errors.
- By using a message broker with Celery, tasks can be processed asynchronously and in parallel, which can improve overall system performance and scalability.
- Message brokers can help to manage high volumes of tasks by buffering messages and allowing them to be processed at a rate that is appropriate for the system, which can help to prevent system overload and ensure that tasks are processed in a timely manner.
- Message brokers can provide additional features and capabilities, such as message routing, filtering, and transformation, which can help to customize the behavior of the task queue and improve overall system flexibility and functionality.

## Why use RabbitMQ?
- RabbitMQ is a widely used and well-established message broker that has been around for over a decade, with a large and active community of users and contributors.
- RabbitMQ supports a wide range of messaging protocols and patterns, including AMQP, MQTT, and STOMP, making it a flexible and versatile choice for many different types of applications.
- RabbitMQ provides a rich set of features and capabilities, including message routing, filtering, and transformation, as well as support for clustering, high availability, and fault tolerance.
- RabbitMQ is highly scalable and can handle large volumes of messages and high levels of traffic, making it a good choice for applications with demanding performance requirements.
- RabbitMQ is open source and free to use, with a permissive license that allows for commercial use and modification.
- Compared to other message brokers such as Apache Kafka or ActiveMQ, RabbitMQ is generally considered to be easier to set up and use, with a more intuitive and user-friendly interface.
- RabbitMQ has a large and active community of users and contributors, which means that there is a wealth of documentation, tutorials, and support available for developers who are new to the platform.
- Celery has built-in support for RabbitMQ, which makes it easy to integrate the two technologies and take advantage of RabbitMQ's features and capabilities.

## Setup RabbitMQ Server and Celery
``` Bash
# Install RabbitMQ Server and Celery
sudo apt install rabbitmq-server celery
# Start RabbitMQ Server
sudo systemctl start rabbitmq-server
# Start Celery Worker
celery -A cubeseed worker --loglevel=info
```

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
    python3 -m venv .venv
    source .venv/bin/activate - # For Mac/Linux
    .venv\Scripts\activate - # For Windows
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


## Run Tests

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