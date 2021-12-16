from confluent_kafka import Producer, Consumer
from time import sleep
import websocket, json


class ExampleProducer:
    broker = "localhost:9092"
    topic = "appmsg"
    producer = None

    def __init__(self):
        self.producer = Producer({
            'bootstrap.servers': self.broker,
            'socket.timeout.ms': 100,
            'api.version.request': 'false',
            'broker.version.fallback': '0.9.0',
        }
        )

    def delivery_report(self, err, msg):
        """ Called once for each message produced to indicate delivery result.
            Triggered by poll() or flush(). """
        if err is not None:
            print('Message delivery failed: {}'.format(err))
        else:
            print('Message delivered to {} [{}]'.format(
                msg.topic(), msg.partition()))

    def send_msg_async(self, msg):
        print("Send message asynchronously")
        self.producer.produce(
            self.topic,
            msg,
            callback=lambda err, original_msg=msg: self.delivery_report(err, original_msg
                                                                        ),
        )
        self.producer.flush()

    def send_msg_sync(self, msg):
        print("Send message synchronously")
        self.producer.produce(
            self.topic,
            msg,
            callback=lambda err, original_msg=msg: self.delivery_report(
                err, original_msg
            ),
        )
        self.producer.flush()

#example_producer = ExampleProducer()
#message = "Hey Mate howdy, mast and bloody good"
#example_producer.send_msg_sync(message)

ws = websocket.WebSocket()
ws.connect("ws://192.168.1.16:8080/appmsg/")
ws.send(json.dumps({'value': "Bhaai Saahab Bhaai Taau Jhonty jee ke Rhodes kee Kasam hain tumhe"}))