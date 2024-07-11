import paho.mqtt.client as mqtt
from database_storage import Database
import json

class MQTTClient:
    def __init__(self, broker, port, topic):
        self.broker = broker
        self.port = port
        self.topic = topic
        self.data_db = Database('data.json')
        self.client = mqtt.Client()

        self.client.username_pw_set("bobm", "letmein")
        self.client.on_message = self.on_message
        self.client.on_connect = self.on_connect

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected with result code {rc}")
        client.subscribe(self.topic)

    def on_message(self, client, userdata, message):
        print("message received:")
        print("message: ", message.payload.decode())
        print("\n")

        try:
            data = json.loads(message.payload.decode())
            self.data_db.store_data(data, message.topic)
        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON: {e}")

    def start(self):
        self.client.connect(self.broker, self.port, 60)
        self.client.loop_forever()

    def stop(self):
        self.client.disconnect()