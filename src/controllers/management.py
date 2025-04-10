from services.mqtt_service import MqttService
from models.event import Event

class ManagementController:
    def __init__(self, mqtt_service: MqttService):
        self.mqtt_service = mqtt_service

    async def handle_event_publish(self, event: Event):
        topic = "test"  
        self.mqtt_service.publish(topic, event)
        return {"message": f"Details of event '{event.payload}' published"}