from paho.mqtt import client as mqtt
from fastapi import BackgroundTasks
import os
from models.control_message import ControlMessage

class MqttService:
    def __init__(self):
        self.broker_url = os.getenv("MQTT_BROKER_URL")
        self.broker_port = int(os.getenv("MQTT_BROKER_PORT", 1884))
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def connect(self):
        self.client.connect(self.broker_url, self.broker_port)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected to MQTT Broker with result code: " + str(rc))

    def on_message(self, client, userdata, msg):
        print(f"Message received on topic {msg.topic}: {msg.payload.decode()}")

    def publish(self, topic: str, message: ControlMessage):
        message_str = str(message)  # Convert message to string
        self.client.publish(topic, message_str)
        return {"message": f"Details of event '{message_str}' published"}

    def subscribe(self, topic: str, background_tasks: BackgroundTasks):
        self.client.subscribe(topic)
        self.client.on_message = lambda client, userdata, msg: background_tasks.add_task(self.on_message, client, userdata, msg)

