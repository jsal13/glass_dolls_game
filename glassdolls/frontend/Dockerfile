FROM python:3.12-slim-bookworm

ENV IN_DOCKER 1
ENV APP_HOME /app
WORKDIR /app

COPY . .

# Install dependency packages
ENV VIRTUAL_ENV=/usr/local
RUN pip install uv && uv pip install --no-cache -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["flask", "--app", "app", "run", "--port", "5000", "--host", "0.0.0.0", "--debug"]