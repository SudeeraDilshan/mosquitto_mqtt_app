from pydantic import BaseModel, Field, model_validator
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum

class ActionType(str, Enum):
    SUSPEND = "SUSPEND"
    RESUME = "RESUME"
    RESTART = "RESTART"
    CONFIGURE = "CONFIGURE"
    RESET_SESSION = "RESET_SESSION"
    REMOVE = "REMOVE"
    TOOL_RELOAD = "TOOL_RELOAD"
    SET_PARAMETERS = "SET_PARAMETERS"

class Priority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

class ControlMessage(BaseModel):
    action_type: ActionType
    agent_id: str
    timestamp: datetime = Field(default_factory=datetime.now)
    priority: Optional[Priority] = None
    payload: Dict[str, Any] = Field(default_factory=dict)
    message_id: Optional[str] = None
    require_ack: bool = True
    ack_timeout: Optional[int] = 30
    retry_on_failure: bool = True

    @model_validator(mode="after")
    def set_default_priority(self) -> "ControlMessage":
        if self.priority is None:
            self.priority = self.get_default_priority()
        return self

    def get_default_priority(self) -> Priority:
        action_priority_map = {
            ActionType.SUSPEND: Priority.HIGH,
            ActionType.RESUME: Priority.MEDIUM,
            ActionType.RESTART: Priority.HIGH,
            ActionType.CONFIGURE: Priority.MEDIUM,
            ActionType.RESET_SESSION: Priority.HIGH,
            ActionType.REMOVE: Priority.HIGH,
            ActionType.TOOL_RELOAD: Priority.MEDIUM,
            ActionType.SET_PARAMETERS: Priority.LOW,
        }
        return action_priority_map.get(self.action_type, Priority.MEDIUM)
