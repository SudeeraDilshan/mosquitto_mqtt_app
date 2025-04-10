# from fastapi import APIRouter
from services.mqtt_service import MqttService
from models.event import Event

class ManagementController:
    def __init__(self, mqtt_service: MqttService):
        self.mqtt_service = mqtt_service
        # self.router = APIRouter()
        # self.router.add_api_route("/event/publish", self.handle_event_publish, methods=["POST"])

    async def handle_event_publish(self, event: Event):
        topic = "test"  
        self.mqtt_service.publish(topic, event)
        return {"message": f"Event of type '{event.get('event_type')}' published"}