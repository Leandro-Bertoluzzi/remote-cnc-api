FROM python:3.9

WORKDIR /app

# Add files from the build context to the container temporarily to execute a RUN instruction
# https://docs.docker.com/develop/develop-images/instructions/#add-or-copy
RUN --mount=type=bind,source=requirements.txt,target=/tmp/requirements.txt \
pip install --no-cache-dir --upgrade -r /tmp/requirements.txt

# Copy project files
COPY . .

# Run uvicorn server
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

# If running behind a proxy like Nginx or Traefik add --proxy-headers
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]
