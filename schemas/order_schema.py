from pydantic import BaseModel, Field, validator
from typing import List, Literal
class OrderSchema(BaseModel):
    order_id: str = Field(..., description="Unique order identifier")
    processing_time: int = Field(..., gt=0, description="Processing time in hours")
    machine_required: str = Literal["CNC Lathe", "3D Printer", "Laser Cutter", "Milling Machine"]
    deadline: int = Field(..., gt=0, description="Deadline in hours from now")
    priority: int = Field(..., ge=1, le=5, description="Priority from 1 (low) to 5 (high)")

class OrdersPayload(BaseModel):
    orders: List[OrderSchema]
