from cg.services.order_validation_service.rules.case.rules import (
    validate_case_internal_ids_exist,
    validate_case_names_available,
    validate_case_names_not_repeated,
    validate_gene_panels_unique,
)
from cg.services.order_validation_service.rules.case_sample.rules import (
    validate_application_compatibility,
    validate_application_exists,
    validate_application_not_archived,
    validate_buffer_skip_rc_condition,
    validate_concentration_interval_if_skip_rc,
    validate_concentration_required_if_skip_rc,
    validate_container_name_required,
    validate_fathers_are_male,
    validate_fathers_in_same_case_as_children,
    validate_gene_panels_exist,
    validate_mothers_are_female,
    validate_mothers_in_same_case_as_children,
    validate_not_all_samples_unknown_in_case,
    validate_pedigree,
    validate_sample_names_different_from_case_names,
    validate_sample_names_not_repeated,
    validate_samples_exist,
    validate_subject_ids_different_from_case_names,
    validate_subject_ids_different_from_sample_names,
    validate_subject_sex_consistency,
    validate_tube_container_name_unique,
    validate_volume_interval,
    validate_volume_required,
    validate_well_position_format,
    validate_well_positions_required,
    validate_wells_contain_at_most_one_sample,
)

MIP_DNA_CASE_RULES: list[callable] = [
    validate_case_internal_ids_exist,
    validate_case_names_available,
    validate_case_names_not_repeated,
    validate_gene_panels_exist,
    validate_gene_panels_unique,
]

MIP_DNA_CASE_SAMPLE_RULES: list[callable] = [
    validate_application_compatibility,
    validate_application_exists,
    validate_application_not_archived,
    validate_buffer_skip_rc_condition,
    validate_volume_required,
    validate_concentration_interval_if_skip_rc,
    validate_concentration_required_if_skip_rc,
    validate_container_name_required,
    validate_fathers_are_male,
    validate_fathers_in_same_case_as_children,
    validate_mothers_are_female,
    validate_mothers_in_same_case_as_children,
    validate_not_all_samples_unknown_in_case,
    validate_pedigree,
    validate_samples_exist,
    validate_sample_names_different_from_case_names,
    validate_sample_names_not_repeated,
    validate_subject_ids_different_from_case_names,
    validate_subject_ids_different_from_sample_names,
    validate_subject_sex_consistency,
    validate_tube_container_name_unique,
    validate_volume_interval,
    validate_well_positions_required,
    validate_wells_contain_at_most_one_sample,
    validate_well_position_format,
]
