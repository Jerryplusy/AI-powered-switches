FROM python:3.13-slim

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . /app

ENV PYTHONPATH=/app
ENV PORT=8000
ENV HOST=0.0.0.0

CMD ["uvicorn", "run:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]