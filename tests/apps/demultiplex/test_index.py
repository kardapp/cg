"""Tests for functions related to indexes."""


import pytest

from cg.apps.demultiplex.sample_sheet.index import (
    INDEX_ONE_PAD_SEQUENCE,
    INDEX_TWO_PAD_SEQUENCE,
    LONG_INDEX_CYCLE_NR,
    Index,
    get_hamming_distance_for_indexes,
    get_index_pair,
    get_reverse_complement_dna_seq,
    get_valid_indexes,
    pad_and_reverse_complement_sample_indexes,
    update_barcode_mismatch_values_for_sample,
)
from cg.apps.demultiplex.sample_sheet.models import (
    FlowCellSampleBcl2Fastq,
    FlowCellSampleBCLConvert,
)
from cg.apps.demultiplex.sample_sheet.sample_sheet_creator import (
    SampleSheetCreatorBCLConvert,
)
from cg.models.demultiplex.run_parameters import RunParameters


def test_get_valid_indexes():
    """Test that the function get_valid_indexes returns a list of Index objects."""
    # GIVEN a sample sheet API

    # WHEN fetching the indexes
    indexes: list[Index] = get_valid_indexes()

    # THEN assert that the indexes are correct
    assert indexes
    assert isinstance(indexes[0], Index)


def test_get_index_pair_valid_cases(
    novaseq6000_flow_cell_sample_before_adapt_indexes: FlowCellSampleBcl2Fastq,
):
    """Test that getting individual indexes from valid dual indexes works."""
    # GIVEN a list of dual indexes and their correct separation into individual indexes
    dual_indexes: list[str] = ["ABC-DEF", "   GHI - JKL   ", "MNO-PQR\n"]
    expected_results: list[tuple[str, str]] = [("ABC", "DEF"), ("GHI", "JKL"), ("MNO", "PQR")]

    # WHEN getting the individual indexes of the valid indexes
    for index, expected in zip(dual_indexes, expected_results):
        novaseq6000_flow_cell_sample_before_adapt_indexes.index = index
        # THEN the result is the expected result for all cases
        assert get_index_pair(sample=novaseq6000_flow_cell_sample_before_adapt_indexes) == expected


def test_get_reverse_complement():
    """Test that getting the reverse complement of a DNA strain returns the correct sequence."""
    # GIVEN a DNA strain and its reverse complement
    dna_strain: str = "ACCTCTGT"
    reversed_complement: str = "ACAGAGGT"

    # WHEN getting the reverse complement of the DNA strain
    returned_reverse_complement: str = get_reverse_complement_dna_seq(dna=dna_strain)

    # THEN the result is the expected
    assert returned_reverse_complement == reversed_complement


def test_get_reverse_complement_not_dna(caplog):
    """Test that using a string without 'A', 'C', 'G' or 'T' fails."""
    # GIVEN a non-DNA strain
    strain: str = "ACCUCTGU"

    # WHEN getting the reverse complement
    with pytest.raises(KeyError):
        # THEN the process fails due to not recognising the unknown nucleotide
        get_reverse_complement_dna_seq(dna=strain)


def test_update_barcode_mismatch_values_for_sample(
    lims_novaseq_bcl_convert_samples: list[FlowCellSampleBCLConvert],
    novaseq_x_flow_cell_sample_before_adapt_indexes: FlowCellSampleBCLConvert,
):
    """Test that the barcode mismatch values are updated for a sample."""
    # GIVEN a list of NovaSeqX samples
    present_index: str = lims_novaseq_bcl_convert_samples[0].index
    # GIVEN a sample
    novaseq_x_flow_cell_sample_before_adapt_indexes.index = present_index
    assert novaseq_x_flow_cell_sample_before_adapt_indexes.barcode_mismatches_1 == 1
    assert novaseq_x_flow_cell_sample_before_adapt_indexes.barcode_mismatches_2 == 1

    # WHEN adapting the barcode mismatch values
    update_barcode_mismatch_values_for_sample(
        sample_to_update=novaseq_x_flow_cell_sample_before_adapt_indexes,
        samples_to_compare_to=lims_novaseq_bcl_convert_samples,
    )

    # THEN the barcode mismatch values have been updated
    assert novaseq_x_flow_cell_sample_before_adapt_indexes.barcode_mismatches_1 == 0
    assert novaseq_x_flow_cell_sample_before_adapt_indexes.barcode_mismatches_2 == 0


def test_update_barcode_mismatch_values_for_sample_comparing_to_self(
    novaseq_x_flow_cell_sample_before_adapt_indexes: FlowCellSampleBCLConvert,
):
    """Test that a sample does not compare to itself when adapting barcode mismatching values."""
    # GIVEN a list of repeated unadapted NovaSeqX samples
    assert novaseq_x_flow_cell_sample_before_adapt_indexes.barcode_mismatches_1 == 1
    assert novaseq_x_flow_cell_sample_before_adapt_indexes.barcode_mismatches_2 == 1
    samples: list[FlowCellSampleBCLConvert] = [
        novaseq_x_flow_cell_sample_before_adapt_indexes for _ in range(3)
    ]

    # WHEN adapting the barcode mismatch values for the samples
    update_barcode_mismatch_values_for_sample(
        sample_to_update=novaseq_x_flow_cell_sample_before_adapt_indexes,
        samples_to_compare_to=samples,
    )

    # THEN the barcode mismatch values remains being 1 for all samples
    for sample in samples:
        assert sample.barcode_mismatches_1 == 1
        assert sample.barcode_mismatches_2 == 1


def test_pad_and_reverse_complement_sample_indexes_reverse_complement_padding(
    bcl_convert_sample_sheet_creator: SampleSheetCreatorBCLConvert,
    novaseq_6000_run_parameters: RunParameters,
    novaseq6000_flow_cell_sample_before_adapt_indexes: FlowCellSampleBcl2Fastq,
):
    """Test that adapting indexes for a sample that needs padding and reverse complement works."""
    # GIVEN a run parameters file that needs reverse complement of indexes
    bcl_convert_sample_sheet_creator.run_parameters = novaseq_6000_run_parameters
    assert bcl_convert_sample_sheet_creator.index_settings.should_i5_be_reverse_complimented
    # GIVEN a sample that needs padding
    sample: FlowCellSampleBcl2Fastq = novaseq6000_flow_cell_sample_before_adapt_indexes
    assert novaseq_6000_run_parameters.get_index_1_cycles() == LONG_INDEX_CYCLE_NR
    sample.index = "ATTCCACA-TGGTCTTG"

    # WHEN adapting the indexes of the sample
    pad_and_reverse_complement_sample_indexes(
        sample=sample,
        index_cycles=novaseq_6000_run_parameters.index_length,
        perform_reverse_complement=bcl_convert_sample_sheet_creator.index_settings.should_i5_be_reverse_complimented,
    )
    # THEN the first index was correctly adapted
    assert len(sample.index) == LONG_INDEX_CYCLE_NR
    assert sample.index[-2:] == INDEX_ONE_PAD_SEQUENCE
    # THEN the second index was correctly adapted
    assert len(sample.index2) == LONG_INDEX_CYCLE_NR
    assert sample.index2[-2:] == get_reverse_complement_dna_seq(dna=INDEX_TWO_PAD_SEQUENCE)


def test_pad_and_reverse_complement_sample_indexes_reverse_complement_no_padding(
    bcl_convert_sample_sheet_creator: SampleSheetCreatorBCLConvert,
    novaseq_6000_run_parameters: RunParameters,
    novaseq6000_flow_cell_sample_before_adapt_indexes: FlowCellSampleBcl2Fastq,
):
    """Test that adapting indexes of a sample that needs reverse complement but no padding works."""
    # GIVEN a run parameters file that needs reverse complement of indexes
    bcl_convert_sample_sheet_creator.run_parameters = novaseq_6000_run_parameters
    assert bcl_convert_sample_sheet_creator.index_settings.should_i5_be_reverse_complimented
    # GIVEN a sample that does not need padding
    sample: FlowCellSampleBcl2Fastq = novaseq6000_flow_cell_sample_before_adapt_indexes
    assert novaseq_6000_run_parameters.get_index_1_cycles() == LONG_INDEX_CYCLE_NR
    assert len(sample.index) >= 2 * LONG_INDEX_CYCLE_NR
    initial_indexes: list[str] = sample.index.split("-")
    initial_index1: str = initial_indexes[0]
    initial_index2: str = initial_indexes[1]

    # WHEN adapting the indexes of the sample
    pad_and_reverse_complement_sample_indexes(
        sample=sample,
        index_cycles=novaseq_6000_run_parameters.index_length,
        perform_reverse_complement=bcl_convert_sample_sheet_creator.index_settings.should_i5_be_reverse_complimented,
    )

    # THEN the first index was correctly adapted
    assert len(sample.index) == LONG_INDEX_CYCLE_NR
    assert sample.index == initial_index1
    # THEN the second index was correctly adapted
    assert len(sample.index2) == LONG_INDEX_CYCLE_NR
    assert sample.index2 == get_reverse_complement_dna_seq(dna=initial_index2)


def test_pad_and_reverse_complement_sample_indexes_no_reverse_complement_no_padding(
    bcl_convert_sample_sheet_creator: SampleSheetCreatorBCLConvert,
    novaseq_x_run_parameters: RunParameters,
    novaseq_x_flow_cell_sample_before_adapt_indexes: FlowCellSampleBCLConvert,
):
    """Test adapting indexes of a sample that does not need reverse complement nor padding works."""
    # GIVEN that the sample sheet creator is for NovaSeqX
    bcl_convert_sample_sheet_creator.run_parameters = novaseq_x_run_parameters
    bcl_convert_sample_sheet_creator.index_settings = (
        bcl_convert_sample_sheet_creator._get_index_settings()
    )
    # GIVEN a run parameters file that does not need reverse complement of indexes
    assert not bcl_convert_sample_sheet_creator.index_settings.should_i5_be_reverse_complimented

    # GIVEN a sample that does not need padding
    sample: FlowCellSampleBCLConvert = novaseq_x_flow_cell_sample_before_adapt_indexes
    assert novaseq_x_run_parameters.get_index_1_cycles() == LONG_INDEX_CYCLE_NR
    assert len(sample.index) >= 2 * LONG_INDEX_CYCLE_NR
    initial_indexes: list[str] = sample.index.split("-")
    initial_index1: str = initial_indexes[0]
    initial_index2: str = initial_indexes[1]

    # WHEN adapting the indexes of the sample
    pad_and_reverse_complement_sample_indexes(
        sample=sample,
        index_cycles=novaseq_x_run_parameters.index_length,
        perform_reverse_complement=bcl_convert_sample_sheet_creator.index_settings.should_i5_be_reverse_complimented,
    )

    # THEN the first index was correctly adapted
    assert len(sample.index) == LONG_INDEX_CYCLE_NR
    assert sample.index == initial_index1

    # THEN the second index was correctly adapted
    assert len(sample.index2) == LONG_INDEX_CYCLE_NR
    assert sample.index2 == initial_index2


def test_get_hamming_distance_index_1_different_lengths():
    """Test that hamming distance between indexes with same prefix but different lengths is zero."""
    # GIVEN two index_1 sequences with the same prefixes but different lengths
    sequence_1: str = "GATTACA"
    sequence_2: str = "GATTACAXX"

    # WHEN getting the hamming distance between them in any order

    # THEN the distance is zero
    assert get_hamming_distance_for_indexes(sequence_1=sequence_1, sequence_2=sequence_2) == 0
    assert get_hamming_distance_for_indexes(sequence_1=sequence_2, sequence_2=sequence_1) == 0

    # WHEN getting the hamming distance between themselves

    # THEN the distance is zero
    assert get_hamming_distance_for_indexes(sequence_1=sequence_1, sequence_2=sequence_1) == 0
    assert get_hamming_distance_for_indexes(sequence_1=sequence_2, sequence_2=sequence_2) == 0


def test_get_hamming_distance_index_1_different_prefixes():
    """Test that hamming distance for index 1 counts different characters from the left."""
    # GIVEN two index_1 sequences with different lengths differing by two characters
    # when aligned to the left
    sequence_1: str = "GATXX"
    sequence_2: str = "GATTACA"

    # WHEN getting the hamming distance between them in any order

    # THEN the distance is equal to the number of different characters
    assert get_hamming_distance_for_indexes(sequence_1=sequence_1, sequence_2=sequence_2) == 2
    assert get_hamming_distance_for_indexes(sequence_1=sequence_2, sequence_2=sequence_1) == 2
