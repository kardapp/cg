from cg.services.order_validation_service.errors.order_errors import OrderError
from cg.services.order_validation_service.errors.sample_errors import SampleError
from cg.services.order_validation_service.errors.validation_errors import ValidationErrors
from cg.services.order_validation_service.order_validation_service import OrderValidationService
from cg.services.order_validation_service.utils import (
    apply_order_validation,
    apply_sample_validation,
)
from cg.services.order_validation_service.workflows.microsalt.validation.field.model_validator import (
    MicroSaltModelValidator,
)
from cg.services.order_validation_service.workflows.microsalt.validation_rules import (
    ORDER_RULES,
    SAMPLE_RULES,
)
from cg.store.store import Store


class MicroSaltValidationService(OrderValidationService):

    def __init__(self, store: Store):
        self.store = store

    def validate(self, raw_order: dict) -> ValidationErrors:
        order, field_errors = MicroSaltModelValidator.validate(raw_order)

        if field_errors:
            return field_errors

        order_errors: list[OrderError] = apply_order_validation(
            rules=ORDER_RULES,
            order=order,
            store=self.store,
        )
        sample_errors: list[SampleError] = apply_sample_validation(
            rules=SAMPLE_RULES,
            order=order,
            store=self.store,
        )

        return ValidationErrors(
            order_errors=order_errors,
            sample_errors=sample_errors,
        )
