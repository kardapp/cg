from cg.services.order_validation_service.rules.sample.rules import (
    validate_application_compatibility,
    validate_application_exists,
    validate_applications_not_archived,
    validate_container_name_required,
    validate_pools_contain_one_application,
    validate_pools_contain_one_priority,
    validate_sample_names_available,
    validate_sample_names_unique,
    validate_volume_interval,
    validate_volume_required,
    validate_well_position_rml_format,
    validate_well_positions_required_rml,
)

RML_SAMPLE_RULES: list[callable] = [
    validate_application_compatibility,
    validate_application_exists,
    validate_applications_not_archived,
    validate_container_name_required,
    validate_pools_contain_one_application,
    validate_pools_contain_one_priority,
    validate_sample_names_available,
    validate_sample_names_unique,
    validate_volume_interval,
    validate_volume_required,
    validate_well_position_rml_format,
    validate_well_positions_required_rml,
]
