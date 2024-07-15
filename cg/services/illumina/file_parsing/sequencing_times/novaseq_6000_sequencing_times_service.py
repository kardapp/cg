"""Module to get the sequencing completed service."""

from datetime import datetime
from pathlib import Path

from cg.models.run_devices.illumina_run_directory_data import IlluminaRunDirectoryData

from cg.utils.files import get_source_modified_time_stamp
from cg.utils.time import format_time_from_ctime


class Novaseq6000SequencingTimesService:
    """Class to get the modified time of the SequenceComplete.txt for novaseq 6000 sequencing runs."""

    @staticmethod
    def get_end_time(run_directory_data: IlluminaRunDirectoryData) -> datetime:
        """Get the sequencer end date and time."""
        file_path: Path = run_directory_data.get_sequence_completed_path
        modified_time = get_source_modified_time_stamp(file_path)
        return format_time_from_ctime(modified_time)

    @staticmethod
    def get_start_time(run_directory_data: IlluminaRunDirectoryData) -> datetime:
        """Get the sequencer start date and time."""
        file_path: Path = run_directory_data.get_sequence_completed_path
        modified_time = get_source_modified_time_stamp(file_path)
        return format_time_from_ctime(modified_time)
