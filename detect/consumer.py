from confluent_kafka import Consumer, Producer
from typing import Optional
from fastapi import FastAPI, File, UploadFile, Response, Request, WebSocket, Depends, status
import json
import numpy as np
import os
from mlprocess import MLProcessing



def saveToDB(image):
    print(image)

BOOTSTRAPURL = ''
BROKERCERTIFICATELOCATION = ''
KAFKAKEY = ''
TOPICKEY = ''
TOPICNAME = ''

kafka_consumer.subscribe(['${TOPICNAME}'])


incomingmsg = kafka_consumer.poll(1.0)
if incomingmsg is None:
    continue
if incomingmsg.error():
    log.error("Consumer error: {}".format(incomingmsg.error()))
    continue
message = incomingmsg.value().decode('utf-8')
jsondata = json.loads(message)
image_string = jsondata.get("Image")
image = MLProcessing.process(image_string)
saveToDB()
