# MLOps: From Models to Production
## Introduction

In the project this week, we will focus on model deployment for the news classification model that we trained in week 1, and evaluated in week 2.

1. [advanced & optional] we will prepare to deploy as a serverless function using AWS Lambda, getting it working locally

## [Step 1] Containerize the application using Docker

1. Build the Docker Image
  
```bash

docker build -t newscls:latest .
```

2. Start the container:

```bash
docker run -it --rm -d --name model -p 8080:8080 newscls:latest
```

2.1 Stop the container:

```bash
docker stop model
```	

### Push commands for ECR

```python
pip install awscli
```
* Authentication
```
aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin xxxx.dkr.ecr.region-1.amazonaws.com
```

Create a registry in ECR
```python
aws ecr create-repository --repository-name repo-name # add your --profile if you have
```

Tag and Push

```bash
docker tag newscls:latest xxxx.dkr.ecr.region-1.amazonaws.com/newscls:latest 
docker push xxxx.dkr.ecr.region-1.amazonaws.com/newscls:latest
```

Then create Lambda function using `Container image`. Optionally you can add API Gateway to the function.