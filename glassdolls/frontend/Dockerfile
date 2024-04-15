# app/Dockerfile

FROM python:3.12-slim-bookworm

ENV APP_HOME /app
WORKDIR /app

COPY . .

# Install dependency packages
ENV VIRTUAL_ENV=/usr/local
RUN pip install uv && uv pip install --no-cache -r requirements.txt

# TODO: Remove the following line after integrating the API.
RUN pip install .

EXPOSE 8501

# HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "/app/glassdolls/frontend/app.py", "--server.port=8501", "--server.address=0.0.0.0"]