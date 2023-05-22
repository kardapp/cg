"""This module parses metrics for files generated by the BCLConvert tool using the Dragen hardware."""
import csv
import xml.etree.ElementTree as ET
import logging
from pathlib import Path
from typing import List, Union, Dict, Callable
from cg.io.controller import ReadFile
from cg.constants.demultiplexing import SampleSheetHeaderColumnNames
from cg.constants.constants import FileFormat
from cg.apps.sequencing_metrics_parser.models.bcl_convert import (
    BclConvertAdapterMetrics,
    BclConvertDemuxMetrics,
    BclConvertQualityMetrics,
    BclConvertRunInfo,
    BclConvertSampleSheetData,
)


LOG = logging.getLogger(__name__)


class BclConvertMetricsParser:
    def __init__(
        self,
        bcl_convert_quality_metrics_file_path: Path,
        bcl_convert_demux_metrics_file_path: Path,
        bcl_convert_adapter_metrics_file_path: Path,
        bcl_convert_sample_sheet_file_path: Path,
        bcl_convert_run_info_file_path: Path,
    ) -> None:
        """Initialize the class."""
        self.quality_metrics_path: Path = bcl_convert_quality_metrics_file_path
        self.demux_metrics_path: Path = bcl_convert_demux_metrics_file_path
        self.adapter_metrics_path: Path = bcl_convert_adapter_metrics_file_path
        self.sample_sheet_path: Path = bcl_convert_sample_sheet_file_path
        self.run_info_path: Path = bcl_convert_run_info_file_path
        self.quality_metrics: List[BclConvertQualityMetrics] = self.parse_metrics_file(
            metrics_file_path=self.quality_metrics_path, metrics_model=BclConvertQualityMetrics
        )
        self.demux_metrics: List[BclConvertDemuxMetrics] = self.parse_metrics_file(
            metrics_file_path=self.demux_metrics_path, metrics_model=BclConvertDemuxMetrics
        )
        self.adapter_metrics: List[BclConvertAdapterMetrics] = self.parse_metrics_file(
            metrics_file_path=self.adapter_metrics_path, metrics_model=BclConvertAdapterMetrics
        )
        self.sample_sheet: List[BclConvertSampleSheetData] = self.parse_sample_sheet_file()
        self.run_info: BclConvertRunInfo = self.parse_run_info_file()

    def parse_metrics_file(
        self, metrics_file_path, metrics_model: Callable
    ) -> List[Union[BclConvertQualityMetrics, BclConvertDemuxMetrics, BclConvertAdapterMetrics]]:
        """Parse specified BCL convert metrics file."""
        LOG.info(f"Parsing BCLConvert metrics file: {metrics_file_path}")
        parsed_metrics: List[
            Union[BclConvertQualityMetrics, BclConvertDemuxMetrics, BclConvertAdapterMetrics]
        ] = []
        metrics_content: List[Dict] = ReadFile.get_content_from_file(
            file_format=FileFormat.CSV, file_path=metrics_file_path, read_to_dict=True
        )
        for sample_metrics_dict in metrics_content:
            parsed_metrics.append(metrics_model(**sample_metrics_dict))
        return parsed_metrics

    def get_nr_of_header_lines_in_sample_sheet(
        self,
    ) -> int:
        """Return the number of header lines in a sample sheet.
        Any lines before and including the line starting with [Data] is considered the header."""
        sample_sheet_content = ReadFile.get_content_from_file(
            FileFormat.CSV, self.sample_sheet_path
        )
        header_line_count: int = 1
        for line in sample_sheet_content:
            if SampleSheetHeaderColumnNames.DATA.value in line:
                break
            header_line_count += 1
        return header_line_count

    def parse_sample_sheet_file(self) -> List[BclConvertSampleSheetData]:
        """Return sample sheet sample lines."""
        LOG.info(f"Parsing BCLConvert sample sheet file: {self.sample_sheet_path}")
        header_line_count: int = self.get_nr_of_header_lines_in_sample_sheet()
        sample_sheet_sample_lines: List[BclConvertSampleSheetData] = []
        with open(self.sample_sheet_path, "r") as sample_sheet_file:
            for _ in range(header_line_count):
                next(sample_sheet_file)
            sample_sheet_content = csv.DictReader(sample_sheet_file)
            for line in sample_sheet_content:
                sample_sheet_sample_lines.append(BclConvertSampleSheetData(**line))
        return sample_sheet_sample_lines

    def parse_run_info_file(self) -> BclConvertRunInfo:
        LOG.info(f"Parsing Run info XML {self.run_info_path}")
        parsed_metrics = BclConvertRunInfo(tree=ET.parse(self.run_info_path))
        return parsed_metrics
