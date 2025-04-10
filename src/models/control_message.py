from pydantic import BaseModel, Field
from typing import Literal, Optional, Dict, Any
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
    action_type: ActionType = Field(..., description="Type of control action")
    agent_id: str = Field(..., description="Unique ID of the agent to control")
    timestamp: datetime = Field(default_factory=datetime.now().isoformat, description="Timestamp of the command")
    priority: Optional[Literal["LOW", "MEDIUM", "HIGH"]] = Field(None, description="Priority of the command")
    payload: Dict[str, Any] = Field(default_factory=dict, description="Additional data for the command")
    message_id: Optional[str] = Field(None, description="Unique ID for command tracking")
    require_ack: bool = Field(default=True, description="Expect agent to confirm execution")
    ack_timeout: Optional[int] = Field(default=30, description="Time in seconds to wait for acknowledgment")
    retry_on_failure: bool = Field(default=True, description="Retry sending message if no ack received")

    def get_default_priority(self) -> str:
        """Map default priority for each action type."""
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

    def __post_init__(self):
        """Set default priority dynamically after initialization."""
        if self.priority is None:
            self.priority = self.get_default_priority()


