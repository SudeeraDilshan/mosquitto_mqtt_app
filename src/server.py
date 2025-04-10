from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.management import ManagementController
from services.mqtt_service import MqttService
import uvicorn

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

# Define routes
@app.post("/event/publish")
async def publish_event(event_data: dict):
    return await management_controller.handle_event_publish(event_data)

if __name__ == "__main__":
    mqtt_service.connect()
    uvicorn.run(app, host="localhost", port=8000)