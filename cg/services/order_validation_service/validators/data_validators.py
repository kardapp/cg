from cg.services.order_validation_service.models.errors import (
    UserNotAssociatedWithCustomerError,
    ValidationError,
)
from cg.services.order_validation_service.models.order import Order
from cg.store.store import Store


def validate_user_customer_association(
    order: Order, store: Store, **kwargs
) -> list[ValidationError]:
    has_access: bool = store.is_user_associated_with_customer(
        user_id=order.user_id,
        customer_internal_id=order.customer_internal_id,
    )

    errors: list[ValidationError] = []
    if not has_access:
        error = UserNotAssociatedWithCustomerError()
        errors.append(error)
    return errors
