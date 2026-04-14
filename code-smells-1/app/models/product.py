from typing import Any

from beanie import Document
from pydantic import BaseModel, ConfigDict, Field


class Product(Document):
    """Catalog row."""

    model_config = ConfigDict(populate_by_name=True)

    name: str
    sku: str
    base_price: float = Field(alias="basePrice")
    product_type: str
    metadata: dict[str, Any] = Field(default_factory=dict)

    class Settings:
        name = "products"


class ProductCreate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name: str
    sku: str
    basePrice: float
    product_type: str
