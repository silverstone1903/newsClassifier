FROM python:3.7-slim

WORKDIR /project

# Copy over contents from local directory to the path in Docker container
COPY . /project/

# Install python requirements from requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# WORKDIR /project/app
EXPOSE 80

# Start uvicorn server
CMD ["uvicorn", "app.server:app", "--host", "0.0.0.0", "--port", "80"]