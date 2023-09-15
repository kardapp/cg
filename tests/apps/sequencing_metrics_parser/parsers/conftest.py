import json
from pathlib import Path
from typing import Dict
import pytest

from cg.constants.demultiplexing import (
    BCL2FASTQ_METRICS_DIRECTORY_NAME,
    BCL2FASTQ_METRICS_FILE_NAME,
)


@pytest.fixture
def raw_bcl2fastq_metrics_data() -> Dict:
    """Example structure of a valid stats.json file containing sequecing metrics generated by bcl2fastq."""
    return {
        "Flowcell": "AB1",
        "RunNumber": 1,
        "RunId": "RUN1",
        "ConversionResults": [
            {
                "LaneNumber": 1,
                "DemuxResults": [
                    {
                        "SampleId": "S1",
                        "NumberReads": 1,
                        "Yield": 100,
                        "ReadMetrics": [{"Yield": 100, "YieldQ30": 90, "QualityScoreSum": 100}],
                    }
                ],
                "Undetermined": {
                    "NumberReads": 5293801,
                    "Yield": 1598727902,
                    "ReadMetrics": [
                        {
                            "ReadNumber": 1,
                            "Yield": 799363951,
                            "YieldQ30": 719898156,
                            "QualityScoreSum": 30157716143,
                            "TrimmedBases": 0,
                        },
                        {
                            "ReadNumber": 2,
                            "Yield": 799363951,
                            "YieldQ30": 615436475,
                            "QualityScoreSum": 27313363301,
                            "TrimmedBases": 0,
                        },
                    ],
                },
            }
        ],
    }


@pytest.fixture
def bcl2fastq_flow_cell_path(tmp_path: Path, raw_bcl2fastq_metrics_data: Dict) -> Path:
    """Directory for flow cell demultiplexed with bcl2fastq with valid stats.json file."""

    valid_dir = Path(tmp_path, "l1t1", BCL2FASTQ_METRICS_DIRECTORY_NAME)
    valid_dir.mkdir(parents=True)
    stats_json_path = Path(valid_dir, BCL2FASTQ_METRICS_FILE_NAME)
    stats_json_path.write_text(json.dumps(raw_bcl2fastq_metrics_data))
    return tmp_path
