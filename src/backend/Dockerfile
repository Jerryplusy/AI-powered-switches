version: '3.13.2'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - redis
    environment:
      - REDIS_URL=redis://redis:6379

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"

  worker:
    build: .
    command: celery -A app.services.task_service worker --loglevel=info
    depends_on:
      - ONBUILD