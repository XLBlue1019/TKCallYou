from paho.mqtt import client as mqtt_client
import random

broker = ""
port = 0
topic = ""
client_id = ""

username = ""
password = ""


def connect_mqtt(on_connect = lambda client, userdata, flags, rc: print("Connected to MQTT Broker!") if rc == 0 else print(f"Failed to connect, return code {rc}")):
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client, on_message = lambda client, userdata, msg: print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")):
    client.subscribe(topic=topic, qos=0)
    client.on_message = on_message

    
def unsubscribe(client: mqtt_client):
    client.on_message = None
    client.unsubscribe(topic)
    

def publish(client: mqtt_client, msg):
    result = client.publish(topic, msg)
    status = result[0]
    return status
