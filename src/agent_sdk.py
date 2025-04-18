import json
import time
from paho.mqtt import client as mqtt
from pydantic import BaseModel, ValidationError
from datetime import datetime
from typing import Literal, Dict, Any, Optional


# Define the ControlMessage schema to match the user story requirements
class ControlMessage(BaseModel):
    type: Literal[
        "SUSPEND", "RESUME", "RESTART", "CONFIGURE", "RESET_SESSION",
        "REMOVE", "TOOL_RELOAD", "SET_PARAMETERS"
    ]
    agent_id: str
    timestamp: datetime
    priority: Literal["LOW", "MEDIUM", "HIGH"]
    payload: Dict[str, Any]
    message_id: Optional[str] = None
    require_ack: bool = True
    ack_timeout: Optional[int] = 30
    retry_on_failure: bool = True


# Define the agent ID to listen for commands targeting this specific agent
AGENT_ID = "agent123"  # Modify per instance


# Action handlers
def handle_suspend(payload: Dict[str, Any]):
    duration = payload.get("duration", 60)
    print(f"Suspending for {duration} seconds...")
    time.sleep(duration)
    print("Resuming operation.")


def handle_configure(payload: Dict[str, Any]):
    if "full" in payload and not payload["full"]:
        updates = payload.get("updates", {})
        print(f"Applying partial configuration: {updates}")
    else:
        print("Applying full configuration update.")


def handle_tool_reload(payload: Dict[str, Any]):
    tools = payload.get("tools", [])
    operation = payload.get("operation", "reload")
    print(f"{operation.capitalize()}ing tools: {', '.join(tools)}")


def handle_set_parameters(payload: Dict[str, Any]):
    parameters = payload.get("parameters", {})
    print(f"Setting parameters: {parameters}")


def handle_message(msg: ControlMessage):
    print(f"[{msg.priority}] Command received: {msg.type} for agent {msg.agent_id}")
    
    if msg.agent_id != AGENT_ID:
        print(f"Command is not for this agent ({AGENT_ID}). Ignoring.")
        return  # Ignore if message is not for this agent
    
    # Dispatch based on command type
    if msg.type == "SUSPEND":
        handle_suspend(msg.payload)
    elif msg.type == "CONFIGURE":
        handle_configure(msg.payload)
    elif msg.type == "TOOL_RELOAD":
        handle_tool_reload(msg.payload)
    elif msg.type == "SET_PARAMETERS":
        handle_set_parameters(msg.payload)
    elif msg.type == "RESTART":
        print("Restarting agent...")
    elif msg.type == "REMOVE":
        print("Removing agent...")
        exit(0)
    elif msg.type == "RESET_SESSION":
        print("Resetting agent session...")


# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc))
    client.subscribe("test")


def on_message(client, userdata, msg):
    try:
        message=msg.payload.decode()
        # payload = json.loads(msg.payload.decode())
        # print(payload)
        # message = ControlMessage(**payload)
        print(f"Received message: {message}")
        # handle_message(message)
    except ValidationError as e:
        print(f"Invalid message format: {e}")
    except Exception as e:
        print(f"Error handling message: {e}")


# MQTT Listener Setup
def start_listener():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    # Connect to the MQTT broker (ensure the broker URL and port match the server)
    broker_url = "localhost"  # Replace with the actual broker URL if needed
    broker_port = 1883  # Replace with the actual broker port if needed
    client.connect(broker_url, broker_port, 60)

    # Subscribe to the topic where messages are published
    topic = "test"  # Replace with the topic used by the server
    client.subscribe(topic)

    print(f"Subscribed to topic: {topic}")
    client.loop_forever()


if __name__ == "__main__":
    print("Starting agent listener...")
    start_listener()
