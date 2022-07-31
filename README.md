# MLOps: From Models to Production
## Introduction

In the project this week, we will focus on model deployment for the news classification model that we trained in week 1, and evaluated in week 2.

1. We will build a simple web application backend using FastAPI and Uvicorn that wraps our trained model, and exposes an endpoint to make predictions on live traffic that is sent to the endpoint.
2. We will learn how to wrap our application in a Linux container using Docker. This is a standard practice when we want to deploy our application in a cloud environment such as AWS or Google Cloud. 
3. We will test our web application and Docker container by sending it live traffic (on our local machine) and logging the model predictions.
4. We will write some integration tests to test our Docker container is running fine before deployment
5. [advanced & optional] we will prepare to deploy as a serverless function using AWS Lambda, getting it working locally

## [Step 1] Download & Install Prerequisites:

### Download the instructions & starter code:


```
project
│   README.md
│   Dockerfile
│   requirements.txt
|   test_app.py
|   __init__.py
└───app
│   │   server.py
│   │   __init__.py
|
└───data
    │   news_classifier.joblib
    |   logs.out
```

Go to the `project` directory from the command line. This will be the home directory for your project. All command line commands that follow are from this directory.


### Install Docker

Download and install Docker. You can follow the steps in [this document](https://docs.docker.com/get-docker/). 

If you are new to Docker, we suggest spending some time to get familiar with the Docker command line and dashboard. Docker's [getting started](https://docs.docker.com/get-started/) page is a good resource.

## [Step 2] Create a FastAPI web application to serve model predictions

1. Before getting started on the web application changes, make sure you can run the starter web server code:

```bash
uvicorn app.server:app
```

You should see an output like:
```bash
INFO:     Started server process [5749]
INFO:     Waiting for application startup.
2022-07-21 20:46:59.898 | INFO     | server:startup_event:109 - Setup completed
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

When you go to `http://127.0.0.1:8000` from a web browser, you should see this text output:
`{"Hello": "World"}`:


2. We are now ready to get started on writing the code! All the required code changes for this project are in `app/server.py`. Comments in this file will help you understand the changes we need to make to create our web application to make model predictions. Once the code changes are done, you can start the web server again using the command from the above step.

3. Test with an example request:

Option 1: Using the web browser. 

Visit `http://127.0.0.1:8000/docs`. You will see a /predict endpoint: 

You can click on "Try it now" which will let you modify the input request. Click on "Execute" to see the model prediction response from the web server:

Option 2: Using the command line.

You can construct the POST request and send it to the web server from another tab in the command line as follows:

```bash

$ curl -X 'POST' \
  'http://127.0.0.1:8000/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "source": "<value>",
  "url": "<value>",
  "title": "<value>",
  "description": "<value>"
}'
```

## [Step 3] Containerize the application using Docker

1. Build the Docker Image
  
```bash

docker build -t newscls:latest .
```

2. Start the container:

```bash

docker run -d --rm --name  model -p 80:80 newscls:latest
```

2.1 Stop the container:

```bash
docker stop model
```	

3. Test the Docker container with an example request:

Option 1: Using the web browser: Visit `http://0.0.0.0/docs` and follow the same guidelines as above.

Option 2: Using the command line:

```bash

$ curl -X 'POST' \
  'http://0.0.0.0/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "source": "<value>",
  "url": "<value>",
  "title": "<value>",
  "description": "<value>"
}'

```

Option 3: Using Postman



## [Step 4] Local testing & examining logs


1. SSH into the container using the container id from above: 

```bash
docker exec -it model /bin/sh
```

2. Tail the logs:
```bash
tail -f data/logs.out
```

2.1 Get container logs:

```bash
docker logs model
# or 
docker logs model -n 10
```

3. Now when you send any request to the web server (from the browser, or another tab in the command line), you can see the log output coming through in `logs.out`. Test the web server with these requests and make sure you can see the outputs in `logs.out`:

```bash
{
  "source": "BBC Technology",
  "url": "http://news.bbc.co.uk/go/click/rss/0.91/public/-/2/hi/business/4144939.stm",
  "title": "System gremlins resolved at HSBC",
  "description": "Computer glitches which led to chaos for HSBC customers on Monday are fixed, the High Street bank confirms."
}
```

```bash
{
  "source": "Yahoo World",
  "url": "http://us.rd.yahoo.com/dailynews/rss/world/*http://story.news.yahoo.com/news?tmpl=story2u=/nm/20050104/bs_nm/markets_stocks_us_europe_dc",
  "title": "Wall Street Set to Open Firmer (Reuters)",
  "description": "Reuters - Wall Street was set to start higher on\Tuesday to recoup some of the prior session's losses, though high-profile retailer Amazon.com  may come under\pressure after a broker downgrade."
}
```

```bash
{
  "source": "New York Times",
  "url": "",
  "title": "Weis chooses not to make pickoff",
  "description": "Bill Belichick won't have to worry about Charlie Weis raiding his coaching staff for Notre Dame. But we'll have to see whether new Miami Dolphins coach Nick Saban has an eye on any of his former assistants."
}
```

```bash
{
  "source": "Boston Globe",
  "url": "http://www.boston.com/business/articles/2005/01/04/mike_wallace_subpoenaed?rss_id=BostonGlobe--BusinessNews",
  "title": "Mike Wallace subpoenaed",
  "description": "Richard Scrushy once sat down to talk with 60 Minutes correspondent Mike Wallace about allegations that Scrushy started a huge fraud while chief executive of rehabilitation giant HealthSouth Corp. Now, Scrushy wants Wallace to do the talking."
}
```

```bash
{
  "source": "Reuters World",
  "url": "http://www.reuters.com/newsArticle.jhtml?type=worldNewsstoryID=7228962",
  "title": "Peru Arrests Siege Leader, to Storm Police Post",
  "description": "LIMA, Peru (Reuters) - Peruvian authorities arrested a former army major who led a three-day uprising in a southern  Andean town and will storm the police station where some of his  200 supporters remain unless they surrender soon, Prime  Minister Carlos Ferrero said on Tuesday."
}
```

```bash
{
  "source": "The Washington Post",
  "url": "http://www.washingtonpost.com/wp-dyn/articles/A46063-2005Jan3.html?nav=rss_sports",
  "title": "Ruffin Fills Key Role",
  "description": "With power forward Etan Thomas having missed the entire season, reserve forward Michael Ruffin has done well in taking his place."
}
```

## [Step 5][Optional] Testing with Pytest

This part is optional. We've built our web application, and containerized it with Docker. But imagine a team of ML engineers and scientists that needs to maintain, improve and scale this service over time. It would be nice to write some tests to ensure we don't regress! 

  1. `Pytest` is a popular testing framework for Python. If you haven't used it before, take a look at [this page](https://docs.pytest.org/en/7.1.x/getting-started.html) to get started and familiarize yourself with this library.
   
  2. How do we test FastAPI applications with Pytest? Glad you asked, here's two resources to help you get started:
    (i) [Introduction to testing FastAPI](https://fastapi.tiangolo.com/tutorial/testing/)
    (ii) [Testing FastAPI with startup and shutdown events](https://fastapi.tiangolo.com/advanced/testing-events/)
  
  3. Head over to `test_app.py` to get started. As you develop the tests using prompts in this file, you can run `pytest` to run the tests.

### Testing with Pytest
<sup>Not all the tests were implemented.</sup>

```bash
 docker exec -it model /bin/sh
```

```python
 pytest test_app.py -sv
```