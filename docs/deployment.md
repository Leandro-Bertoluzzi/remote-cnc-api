# Set up API in production with Docker

This guide assumes you want to install and use the app in a Raspberry Pi.

The steps described in this guide were tested in the following device:
- **Board:** Raspberry Pi 3B+
- **OS:** Raspberry Pi OS (Bullseye, 32-bit)

## Build and push a multi-architecture Docker image

If we have made changes to the code, we must generate a Docker image for the architecture of the Raspberry (ARM 32 v7) before starting our environment with `docker compose up`. The easiest method to achieve that is by [using buildx](https://docs.docker.com/build/building/multi-platform/#multiple-native-nodes).

**The first time** we generate the image, we must create a custom builder.

```bash
docker buildx create --name raspberry --driver=docker-container
```

Then, the command to actually generate the images is the following:

```bash
docker buildx build --platform linux/arm/v7,linux/amd64 --tag {{your_dockerhub_user}}/cnc-api:latest --builder=raspberry --target production --push .
```

## Start the API

Starting the API with `docker compose` also sets up a DB and a message broker for Celery, plus an `adminer` instance.

```bash
$ docker compose -f docker-compose.yaml -f docker-compose.production.yaml up -d
```

**NOTE:** We do not use the `--profile=ngrok` parameter because the ngrok service will be run locally, so we can place it "after" the Nginx reverse proxy. If you don't want to install and configure Nginx, just run the command with the `--profile=ngrok` parameter and the API will be publicly available.

## Set up database

Once opened the connection with the DB, you must update its schema by running the file `rpi/db_schema.sql`. You can run it with `adminer`.

# Start the Celery worker

In order to execute tasks and scheduled tasks, you must start the CNC worker (Celery).

```bash
# 1. Move to worker folder
$ cd core/worker

# 2. Start Celery's worker server
$ celery --app tasks worker --loglevel=INFO --logfile=logs/celery.log
```

# (Optional) Set up reverse proxy

Setting up a reverse proxy is certainly not mandatory, but it allows us to:
- Add HTTPS support to improve security.
- Configure redirections (HTTP 30x), useful if we want to modify a URL and still have access to it.
- Rename routes, for example “URL:8000/base” to “URL/api”.
- Use authentication and authorization previous to the endpoint.
- Enforce correct spelling of routes, for example enable “URL/login” but avoid “URL/login/”.
- Add a maintenance mode: Optionally show a fixed response when we are working on the API/Docker and the API is "down".

If you wonder why we don't run Nginx as a container, you can read an article justifying our philosofy [here](https://nickjanetakis.com/blog/why-i-prefer-running-nginx-on-my-docker-host-instead-of-in-a-container).

Moving forward, installing and configuring Nginx is pretty straightforward:

1. Install Nginx
```bash
sudo apt update
sudo apt install nginx
```
2. Copy the file `nginx/api.conf` in this repository to the folder `/etc/nginx` in your Raspberry Pi.
3. In your raspberry, open the file `/etc/nginx/nginx.conf` and add the following line inside the `http` section.
```bash
include /etc/nginx/api.conf; # All API configuration
```
4. Restart Nginx
```bash
sudo systemctl restart nginx
```

# Remote access with ngrok

## With Nginx (recommended)

If we are using Nginx as a reverse proxy, we must run Ngrok outside a container because otherwise we couldn't expose Nginx' port to the outside world.

1. Install the Ngrok client from [Ngrok downloads](https://ngrok.com/download) page, you can either download a zip and unzip it or use `apt install`.
2. Register Ngrok client, with the auth token in your [Ngrok profile](https://dashboard.ngrok.com/get-started/your-authtoken). If you don't have an account, create one.
```bash
ngrok authtoken {{NGROK_AUTHTOKEN}}
```
3. Start the ngrok client with a static domain. If you don't have one, you can create it [in your profile](https://dashboard.ngrok.com/get-started/your-authtoken).
```bash
ngrok http --domain={{NGROK_DOMAIN}} 80 --scheme http,https
```

## Without Nginx

Just (re)run the `docker compose` file with the `ngrok` profile enabled.

```bash
$ docker compose -f docker-compose.yaml -f docker-compose.production.yaml--profile=ngrok up -d
```
