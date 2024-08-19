from pydantic import BaseModel

from cg.services.order_validation_service.errors.case_errors import CaseError
from cg.services.order_validation_service.errors.case_sample_errors import CaseSampleError
from cg.services.order_validation_service.errors.order_errors import OrderError
from cg.services.order_validation_service.errors.sample_errors import SampleError


class ValidationErrors(BaseModel):
    order_errors: list[OrderError] = []
    case_errors: list[CaseError] = []
    sample_errors: list[SampleError] = []
    case_sample_errors: list[CaseSampleError] = []
