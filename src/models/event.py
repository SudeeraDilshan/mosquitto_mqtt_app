from pydantic import BaseModel, Field
from typing import Any, Dict
from datetime import datetime
import uuid

class Event(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))  # Auto-generated event_id
    event_type: str
    payload: Dict[str, Any]
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())