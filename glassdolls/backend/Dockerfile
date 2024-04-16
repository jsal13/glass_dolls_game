# app/Dockerfile

FROM python:3.12-slim-bookworm

ENV IN_DOCKER 1
ENV APP_HOME /app
WORKDIR /app

COPY . .

# Install dependency packages
ENV VIRTUAL_ENV=/usr/local
RUN pip install uv && uv pip install --no-cache -r requirements.txt

EXPOSE 8001

# HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["uvicorn", "api:api", "--port", "8001", "--host", "0.0.0.0", "--reload"]

# uvicorn backend.main:api --port 8081 --host 0.0.0.0