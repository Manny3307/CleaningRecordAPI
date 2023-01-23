from confluent_kafka import Producer, Consumer
from time import sleep
import json, socket
from kafka import KafkaProducer


global KafkaCleaningRecordsBroker, KafkaCleaningRecordsTopic, KafkaCleaningRecordsProducer, KafkaCleaningRecordsGroupID

# Load the Config JSON file from the config folder and read the respective values
KafkaConfigJSON = open('./cleaning_rec/Config/KafkaConfig.json')
KafkaConfigData = json.load(KafkaConfigJSON)

# Get The Base Path from the Config File.

KafkaCleaningRecordsBroker = KafkaConfigData["kafka_configs"]["Cleaning_Records_Kafka_Broker"]
KafkaCleaningRecordsTopic = KafkaConfigData["kafka_configs"]["Cleaning_Records_Kafka_Topic"]
KafkaCleaningRecordsProducer = KafkaConfigData["kafka_configs"]["Cleaning_Records_Kafka_Producer"]
KafkaCleaningRecordsGroupID = KafkaConfigData["kafka_configs"]["Cleaning_Records_Kafka_Group_ID"]

class KafkaFunctions:

    def __init__(self):
        pass
    
    def produce_kafka_message(self, message_str):
        my_consumer = CleaningRecordsMessageProducer()
        my_consumer.send_msg_sync(message_str.encode('utf-8'))

class CleaningRecordsMessageProducer:

    broker = KafkaCleaningRecordsBroker
    topic = KafkaCleaningRecordsTopic
    producer = None

    def __init__(self):
        self.producer = Producer({
            'bootstrap.servers': self.broker,
            'socket.timeout.ms': 100,
            'api.version.request': 'false',
            'broker.version.fallback': '0.9.0',
       })

    def delivery_report(self, err, msg):
        """ Called once for each message produced to indicate delivery result.
            Triggered by poll() or flush(). """
        if err is not None:
            print('Message delivery failed: {}'.format(err))
        else:
            print('Message delivered to {} [{}]'.format(
                msg.topic(), msg.partition()))

    def send_msg_async(self, msg):
        
        self.producer.produce(
            self.topic,
            msg,
            callback=lambda err, original_msg=msg: self.delivery_report(err, original_msg
                                                                        ),
        )
        self.producer.flush()

    def send_msg_sync(self, msg):
        
        self.producer.produce(
            self.topic,
            msg,
            callback=lambda err, original_msg=msg: self.delivery_report(
                err, original_msg
            ),
        )
        self.producer.flush()

class CleaningRecordsMessageConsumer:
    broker = KafkaCleaningRecordsBroker
    topic = KafkaCleaningRecordsTopic
    group_id = KafkaCleaningRecordsGroupID

    def start_listener(self):
        consumer_config = {
            'bootstrap.servers': self.broker,
            'group.id': self.group_id,
            'auto.offset.reset': 'largest',
            'enable.auto.commit': 'false',
            'max.poll.interval.ms': '86400000'
        }

        consumer = Consumer(consumer_config)
        consumer.subscribe([self.topic])

        try:
            while True:
                # read single message at a time
                msg = consumer.poll(0)
                

                if msg is None:
                    sleep(3)
                    continue
                if msg.error():
                    print("Error reading message : {}".format(msg.error()))
                    continue
                # You can parse message and save to data base here
                print(msg.value())
                consumer.commit()

        except Exception as ex:
            print("Kafka Exception : {}", ex)

        finally:
            print("closing consumer")
            consumer.close()