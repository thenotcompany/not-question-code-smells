FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /work

COPY pyproject.toml README.md ./
COPY app ./app

RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir .

EXPOSE 8080
CMD ["/bin/sh", "-c", "exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}"]
