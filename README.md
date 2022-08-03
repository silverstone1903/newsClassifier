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
Create a registry in ECR
```python
aws ecr create-repository --repository-name repo-name # add your --profile if you have
```

* Authentication
```
aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin xxxx.dkr.ecr.region-1.amazonaws.com
```


Tag and Push

```bash
docker tag newscls:latest xxxx.dkr.ecr.region-1.amazonaws.com/newscls:latest 
docker push xxxx.dkr.ecr.region-1.amazonaws.com/newscls:latest
```

Then create Lambda function using `Container image`. Optionally you can add API Gateway to the function.



### Test API Gateway Endpoint

Lambda function just takes `description`, no need to other variables (no logging etc.)

```python
import requests
import pprint
pp = pprint.PrettyPrinter(indent=4)

url = "https://uacqaayaij.execute-api.eu-central-1.amazonaws.com/api/predict"
data = {
    "description": "A capsule carrying solar material from the Genesis space probe has made a crash landing at a US Air Force training facility in the US state of Utah."
}
result = requests.post(url, json=data).json()
pp.pprint(result)

```
