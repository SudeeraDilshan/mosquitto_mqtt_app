from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services.mqtt_service import MqttService
import uvicorn
from models.control_message import ControlMessage
from controllers.helpers import fetch_services_data

app = FastAPI()

# CORS middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize MQTT service
mqtt_service = MqttService()

# Define routes
@app.post("/action")
async def publish_event(event_data: ControlMessage):
    return await mqtt_service.publish(topic="test",message=event_data)

@app.get("/service")
async def get_consul_services():
    response = await fetch_services_data()
    return response


if __name__ == "__main__":
    mqtt_service.connect()
    uvicorn.run(app, host="localhost", port=8000)