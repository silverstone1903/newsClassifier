from app import *
import json
import os


global log_file
global classifier

classifier = NewsCategoryClassifier(GLOBAL_CONFIG)


def lambda_handler(event, context):
    source = event["source"]
    url = event["url"]
    title = event["title"]
    description = event["description"]
    pred = classifier.predict_label(description)[0]
    return pred
