from confluent_kafka import Producer, Consumer
from time import sleep
import websocket, json, socket
from kafka import KafkaProducer, KafkaConsumer
import boto3

conf = {'bootstrap.servers': "localhost:9092",
        'client.id': socket.gethostname()}


class testproducer:
    
    def msgsend(self):
        str = 'Hey'
        producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
        producer.send('appmsg', str.encode('utf-8'))

class ExampleProducer:
    broker = "172.25.0.3:9092"
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

'''example_producer = ExampleProducer()
message = "Hey Mate howdy, mast and bloody good 1"
example_producer.send_msg_sync(message)
'''
#ws = websocket.WebSocket()
#ws.connect("ws://192.168.1.16:8080/appmsg/")
#ws.send(json.dumps({'value': "Bhaai Saahab Bhaai Taau Jhonty jee ke Rhodes kee Kasam hain tumhe"}))

def send_sms():
    client = boto3.client(
        "sns",
        aws_access_key_id='AKIATX24DE6HWLFBYSFH',
        aws_secret_access_key='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',
        region_name="ap-southeast-2"
    )

    client.publish(
        PhoneNumber="+61416438047",
        Message="Message from Manny and Angel"
    )


send_sms()