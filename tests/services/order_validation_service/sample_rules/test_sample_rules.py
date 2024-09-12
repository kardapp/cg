from cg.models.orders.sample_base import ContainerEnum
from cg.services.order_validation_service.errors.sample_errors import (
    ContainerNameRepeatedError,
    SampleNameNotAvailableError,
    WellFormatError,
)
from cg.services.order_validation_service.rules.sample.rules import (
    validate_tube_container_name_unique,
    validate_sample_names_available,
    validate_well_position_format,
)
from cg.services.order_validation_service.workflows.microsalt.models.order import (
    MicrosaltOrder,
)
from cg.store.models import Sample
from cg.store.store import Store


def test_sample_names_available(valid_order: MicrosaltOrder, sample_store: Store):

    # GIVEN an order with a sample name reused from a previous order
    sample = sample_store.session.query(Sample).first()
    valid_order.customer = sample.customer.internal_id
    valid_order.samples[0].name = sample.name

    # WHEN validating that the sample names are available to the customer
    errors = validate_sample_names_available(order=valid_order, store=sample_store)

    # THEN an error should be returned
    assert errors

    # THEN the error should concern the reused sample name
    assert isinstance(errors[0], SampleNameNotAvailableError)


def test_validate_tube_container_name_unique(valid_order: MicrosaltOrder):

    # GIVEN an order with three samples in tubes with 2 reused container names
    valid_order.samples[0].container = ContainerEnum.tube
    valid_order.samples[1].container = ContainerEnum.tube
    valid_order.samples[2].container = ContainerEnum.tube
    valid_order.samples[0].container_name = "container_name"
    valid_order.samples[1].container_name = "container_name"
    valid_order.samples[2].container_name = "ContainerName"

    # WHEN validating the container names are unique
    errors = validate_tube_container_name_unique(order=valid_order)

    # THEN the error should concern the reused container name
    assert isinstance(errors[0], ContainerNameRepeatedError)
    assert errors[0].sample_index == 0
    assert errors[1].sample_index == 1


def test_validate_well_position_format(valid_order: MicrosaltOrder):

    # GIVEN an order with a sample with an invalid well position
    valid_order.samples[0].well_position = "J:4"

    # WHEN validating the well position format
    errors = validate_well_position_format(order=valid_order)

    # THEN an error should be returned
    assert errors

    # THEN the error should concern the invalid well position
    assert isinstance(errors[0], WellFormatError)
    assert errors[0].sample_index == 0
