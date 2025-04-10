from pydantic import BaseModel, Field
from typing import Any, Dict
from datetime import datetime

class Event(BaseModel):
    event_type: str
    payload: Dict[str, Any]
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())