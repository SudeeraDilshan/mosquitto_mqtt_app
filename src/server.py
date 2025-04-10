from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.management import ManagementController
from services.mqtt_service import MqttService
import uvicorn
from models.event import Event
import requests

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

# Initialize Management Controller
management_controller = ManagementController(mqtt_service)

def fetch_services_data():
    """
    Fetch data from the Consul agent services endpoint.
    """
    url = "http://127.0.0.1:8500/v1/agent/services"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}

# Define routes
@app.post("/event/publish")
async def publish_event(event_data: Event):
    return await management_controller.handle_event_publish(event_data)

@app.get("/consul/services")
async def get_consul_services():
    return await management_controller.get_consul_services()


if __name__ == "__main__":
    mqtt_service.connect()
    uvicorn.run(app, host="localhost", port=8000)