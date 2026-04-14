from typing import Any, Optional

from beanie import Document
from pydantic import BaseModel, ConfigDict, Field


class LineItem(BaseModel):
    product_id: str
    qty: int
    unit_price: float


class Order(Document):
    model_config = ConfigDict(populate_by_name=True)

    customer_email: str = Field(alias="customerEmail")
    line_items: list[LineItem] = Field(default_factory=list)
    status: str = "draft"
    raw_payload: Optional[dict[str, Any]] = None

    class Settings:
        name = "orders"


class OrderCreate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    customerEmail: str
    line_items: list[LineItem]
