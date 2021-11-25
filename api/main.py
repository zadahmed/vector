from confluent_kafka import Consumer, Producer
from typing import Optional
from fastapi import FastAPI, File, UploadFile, Response, Request, WebSocket, Depends, status
import json
import cv2
import numpy as np
from google.cloud import pubsub_v1
import os

app = FastAPI()

#invoked when api starts
@app.on_event("startup")
async def startup_event():

    # Kafka Config
    global kafka_consumer
    global producer

    producer = Producer({
        'bootstrap.servers': '${BOOTSTRAPURL}',
        'security.protocol': 'ssl',
        'ssl.certificate.location' :'${BROKERCERTIFICATELOCATION}',
        'ssl.key.location': '${KAFKAKEY}'
        })
    kafka_consumer = Consumer({
       'bootstrap.servers': '${BOOTSTRAPURL}',
        'security.protocol': 'ssl',
        'ssl.certificate.location' :'${BROKERCERTIFICATELOCATION}',
        'ssl.key.location': '${KAFKAKEY}'
    })


    # Google PUB SUB Config
    global project_id = "your-project-id"
    global topic_id = "your-topic-id"
    global publisher = pubsub_v1.PublisherClient()
    




#Kafka producer function to recieve images
@app.websocket("/send/image/data/{TOPICNAME}/{KEY}")
async def kafkaproducer(TOPICNAME, KEY, websocket: WebSocket):
    await websocket.accept()
    BOOTSTRAPURL = ''
    BROKERCERTIFICATELOCATION = ''
    KAFKAKEY = ''
    while True:
        jsondata = await websocket.receive_json()
        if 'Image' not in jsondata:
            jsondata = "Image does not exist in the JSON Body"
            await websocket.send_json({'ERROR': jsondata})
            return
        else:
            producer.produce('${TOPICNAME}', key='${TOPICKEY}', value=json.dumps(jsondata))
            producer.flush()   
            await websocket.send_json({ORGID: jsondata})


#kafka consumer function to store images
@app.websocket("/recieve/image/data/{TOPICNAME}/{KEY}")
async def kafkaconsumer(str: TOPICNAME, str: KEY, websocket: WebSocket):
    BOOTSTRAPURL = ''
    BROKERCERTIFICATELOCATION = ''
    KAFKAKEY = ''
    kafka_consumer.subscribe(['${TOPICNAME}'])
    while True:
        incomingmsg = kafka_consumer.poll(1.0)
        if incomingmsg is None:
            continue
        if incomingmsg.error():
            log.error("Consumer error: {}".format(incomingmsg.error()))
            continue
        message = incomingmsg.value().decode('utf-8')
        jsondata = json.loads(message)
        if 'Image' not in jsondata:
            jsondata = "Image does not exist in the JSON Body"
            await websocket.send_json({'ERROR': jsondata})
            return
        else:
            image_string = jsondata.get("Image")
            data = image_string.split("base64,")
            nparr = np.fromstring(base64.b64decode(data[1]), np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            #store image to db
            print(image)



#Google producer function to recieve images
@app.websocket("/send/google/image/data/{TOPICNAME}/{KEY}")
async def googlepub(str: TOPICNAME, str: KEY, websocket: WebSocket):
    await websocket.accept()
    while True:
        jsondata = await websocket.receive_json()
        if 'Image' not in jsondata:
            jsondata = "Image does not exist in the JSON Body"
            await websocket.send_json({'ERROR': jsondata})
            return
        else:
            topic_name = 'projects/{project_id}/topics/{TOPICNAME}'.format(
                project_id=os.getenv('GOOGLE_CLOUD_PROJECT'),
                topic=TOPICNAME,  # Set this to something appropriate.
            )
            future = publisher.publish(topic_name, jsondata, spam=KEY)
            future.result()
            print(future.result())


#Google consumer function to store images
@app.websocket("/recieve/google/image/data/{TOPICNAME}/{SUB}")
async def googlesub(str: TOPICNAME, str: SUB, websocket: WebSocket):
    topic_name = 'projects/{project_id}/topics/{TOPICNAME}'.format(
    project_id=os.getenv('GOOGLE_CLOUD_PROJECT'),
    topic=TOPICNAME,  
    )
    subscription_name = 'projects/{project_id}/subscriptions/{SUB}'.format(
        project_id=os.getenv('GOOGLE_CLOUD_PROJECT'),
        sub=SUB,  
    )
    with pubsub_v1.SubscriberClient() as subscriber:
        subscriber.create_subscription(
            name=subscription_name, topic=topic_name)
        future = subscriber.subscribe(subscription_name, callback)
        jsondata = json.loads(future.result())
        if 'Image' not in jsondata:
            jsondata = "Image does not exist in the JSON Body"
            await websocket.send_json({'ERROR': jsondata})
            return
        else:
            image_string = jsondata.get("Image")
            data = image_string.split("base64,")
            nparr = np.fromstring(base64.b64decode(data[1]), np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            #store image to db
            print(image)


#invoked when api is shutdown
@app.on_event("shutdown")
async def shutdown_event():
    try:
        producer.close()
        kafka_consumer.close()
    except Exception as e:
        print(e)