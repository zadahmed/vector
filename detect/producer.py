from confluent_kafka import Consumer, Producer
from typing import Optional
from fastapi import FastAPI, File, UploadFile, Response, Request, WebSocket, Depends, status
import json
import cv2
import numpy as np
import os

BOOTSTRAPURL = ''
BROKERCERTIFICATELOCATION = ''
KAFKAKEY = ''
TOPICKEY = ''
TOPICNAME = ''


producer = Producer({
        'bootstrap.servers': '${BOOTSTRAPURL}',
        'security.protocol': 'ssl',
        'ssl.certificate.location' :'${BROKERCERTIFICATELOCATION}',
        'ssl.key.location': '${KAFKAKEY}'
        })
producer.produce('${TOPICNAME}', key='${TOPICKEY}', value=json.dumps(jsondata))
producer.flush()   
