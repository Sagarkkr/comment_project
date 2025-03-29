# Dockerfile
FROM python:3.10


ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y \
build-essential \
libpq-dev \
&& rm -rf /var/lib/apt/lists/*


RUN mkdir comment

WORKDIR /comment

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN python manage.py collectstatic --noinput

RUN python manage.py migrate 

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "comment.wsgi:application"]
