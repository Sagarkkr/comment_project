# AI-powered Moderation Microservice

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)

A microservice that scans user-generated content for inappropriate content using AI and flags it for moderation. Built with Django, PostgreSQL, and Docker.

## Features

- ✅ User authentication 
- 📝 Content submission with AI moderation
- 🚩 Flagged content storage
- 📊 Admin dashboard for moderation
- 🐳 Dockerized deployment

## Tech Stack

- **Backend**: Django + Django REST Framework
- **Database**: PostgreSQL
- **AI Moderation**: Perspective API by Google cloud
- **Containerization**: Docker

## Prerequisites

- Python 3.9+
- Docker
- PostgreSQL
- Perspective API key (free from [Google Cloud](https://cloud.google.com/natural-language/docs/moderating-text))

## Installation

### 1. Clone the repository
```bash
git clone git@github.com:Sagarkkr/comment_project.git
```
### 2. Create virtual environment
```
python -m venv {env_name}
```
### 3. Move to project folder
```
cd comment/
```
### 4. Run migrations
```
python manage.py migrate
```
### 5. Create superuser
```
python manage.py createsuperuser
```
### 6. Final step run the server
```
python manage.py runserver
```