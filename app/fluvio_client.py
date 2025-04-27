import os
import json
from fluvio import Fluvio, FluvioConfig
from flask import current_app

class FluvioClient:
    def __init__(self):
        self.client = None
        self.connect()
        
    def connect(self):
        try:
            config = FluvioConfig()
            self.client = Fluvio.connect(config)
        except Exception as e:
            current_app.logger.error(f"Error connecting to Fluvio: {str(e)}")
            raise
            
    def produce_message(self, topic, message):
        try:
            producer = self.client.topic_producer(topic)
            producer.send_string(json.dumps(message))
        except Exception as e:
            current_app.logger.error(f"Error producing message to Fluvio: {str(e)}")
            raise
            
    def consume_messages(self, topic, consumer_group):
        try:
            consumer = self.client.partition_consumer(topic, 0)
            while True:
                record = consumer.next()
                if record:
                    yield json.loads(record.value_string())
        except Exception as e:
            current_app.logger.error(f"Error consuming messages from Fluvio: {str(e)}")
            raise
            
    def stream_data(self, topic, consumer_group):
        try:
            consumer = self.client.partition_consumer(topic, 0)
            while True:
                record = consumer.next()
                if record:
                    yield json.loads(record.value_string())
        except Exception as e:
            current_app.logger.error(f"Error streaming data from Fluvio: {str(e)}")
            raise 