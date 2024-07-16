from pydantic import BaseModel, Field

from cg.constants import DataDelivery
from cg.constants.constants import Workflow

TICKET_PATTERN = r"^#\d{4,}"


class Order(BaseModel):
    comment: str | None = None
    connect_to_ticket: bool = False
    customer_internal_id: str = Field(alias="customer")
    delivery_type: DataDelivery
    name: str
    skip_reception_control: bool = False
    ticket_number: str | None = Field(None, pattern=TICKET_PATTERN)
    user_id: int
    workflow: Workflow
