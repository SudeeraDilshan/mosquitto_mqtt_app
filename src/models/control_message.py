from pydantic import BaseModel, Field, model_validator
from typing import Optional, Dict, Any, Literal
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

class ControlMessage(BaseModel):
    action_type: ActionType
    agent_id: str
    timestamp: datetime = Field(default_factory=datetime.now)
    priority: Optional[Literal["LOW", "MEDIUM", "HIGH"]] = None
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

    def get_default_priority(self) -> str:
        action_priority_map = {
            ActionType.SUSPEND: "HIGH",
            ActionType.RESUME: "MEDIUM",
            ActionType.RESTART: "HIGH",
            ActionType.CONFIGURE: "MEDIUM",
            ActionType.RESET_SESSION: "HIGH",
            ActionType.REMOVE: "HIGH",
            ActionType.TOOL_RELOAD: "MEDIUM",
            ActionType.SET_PARAMETERS: "LOW",
        }
        return action_priority_map.get(self.action_type, "MEDIUM")
