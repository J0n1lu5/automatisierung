import paho.mqtt.client as mqtt
from database_storage import Database
import json


class MQTTClient:
    def __init__(self, broker, port, topic, username=None, password=None):
        self.broker = broker
        self.port = port
        self.topic = topic
        self.username = username
        self.password = password
        self.data_db = Database('data.json')
        self.client = mqtt.Client()

        if self.username and self.password:
            self.client.username_pw_set(self.username, self.password)

        self.client.on_message = self.on_message
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected successfully.")
            client.subscribe(self.topic)
        else:
            print(f"Connection failed with code {rc}")

    def on_disconnect(self, client, userdata, rc):
        print("Disconnected from MQTT broker")
        if rc != 0:
            print("Unexpected disconnection.")

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
        try:
            self.client.connect(self.broker, self.port, 60)
            self.client.loop_forever()
        except Exception as e:
            print(f"Error connecting to MQTT broker: {e}")

    def stop(self):
        self.client.disconnect()
