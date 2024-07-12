import paho.mqtt.client as mqtt
import time
import signal
import sys
import json

class MQTTClient:
    def __init__(self, broker, port, topic, data_file='received_data.json'):
        self.broker = broker
        self.port = port
        self.topic = topic
        self.data_file = data_file
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
            self.client.subscribe(self.topic)
        else:
            print("Failed to connect, return code %d\n", rc)

    def on_message(self, client, userdata, msg):
        message = msg.payload.decode()
        print(f"Received message: {message} on topic {msg.topic}")
        self.save_message(message)

    def save_message(self, message):
        try:
            with open(self.data_file, 'a') as file:
                file.write(message + '\n')
        except Exception as e:
            print(f"Error saving message: {e}")

    def start(self):
        self.client.connect(self.broker, self.port, 60)
        self.client.loop_forever()

    def stop(self):
        self.client.disconnect()

def signal_handler(sig, frame):
    print('Stopping MQTT Receiver...')
    sys.exit(0)