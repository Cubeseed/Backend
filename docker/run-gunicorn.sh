#!/bin/sh

gunicorn -w 5 -b 0.0.0.0:8000 cubeseed.wsgi