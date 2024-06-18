import paho.mqtt.client as mqtt
from database_storage import Database
import json


broker = "158.180.44.197"
port = 1883
topic = "iot1/teaching_factory_fast/#"

print("Connecting to broker", broker)

data_db = Database('data.json')


# create function for callback
def on_message(client, userdata, message):
    print("message received:")
    print("message: ", message.payload.decode())
    print("\n")
    
    # for jedes topic wird eine eigene Tabelle erstellt

    #db.insert(message.topic, message.payload.decode())
    try:
        data = json.loads(message.payload.decode())
        #topic_name = json.loads(message.topic)
        data_db.store_data(data, message.topic)
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON: {e}")

# create client object
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.username_pw_set("bobm", "letmein")              

# assign function to callback
mqttc.on_message = on_message                          

# establish connection
mqttc.connect(broker,port)                                 
print("Connected to broker")
# subscribe
mqttc.subscribe(topic, qos=0)

# Blocking call that processes network traffic, dispatches callbacks and handles reconnecting.
#mqttc.loop_forever()

while True:
    mqttc.loop(0.5)
    
