from pydantic import BeforeValidator
from typing_extensions import Annotated

from cg.models.orders.sample_base import ControlEnum, PriorityEnum
from cg.services.order_validation_service.models.sample import Sample
from cg.services.order_validation_service.utils import parse_control


class RmlSample(Sample):
    control: Annotated[ControlEnum, BeforeValidator(parse_control)] = ControlEnum.not_control
    index: str
    index_number: int
    pool: str
    pool_concentration: float
    priority: PriorityEnum
    rml_plate_name: str | None = None
    sample_concentration: float | None = None
    volume: int
    well_position_rml: str | None = None
