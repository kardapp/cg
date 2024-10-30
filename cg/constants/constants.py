"""Constants for cg."""

from enum import Enum, IntEnum, StrEnum, auto

from cg.utils.date import get_date

VALID_DATA_IN_PRODUCTION = get_date("2017-09-27")

LENGTH_LONG_DATE: int = len("YYYYMMDD")

MAX_ITEMS_TO_RETRIEVE = 50

SCALE_TO_MILLION_READ_PAIRS = 2_000_000
SCALE_TO_READ_PAIRS = 2

ANALYSIS_TYPES = ["tumor_wgs", "tumor_normal_wgs", "tumor_panel", "tumor_normal_panel"]

CAPTUREKIT_CANCER_OPTIONS = (
    "GIcfDNA",
    "GMCKsolid",
    "GMSmyeloid",
    "LymphoMATIC",
    "other (specify in comment field)",
)
CAPTUREKIT_OPTIONS = (
    "Agilent Sureselect CRE",
    "Agilent Sureselect V5",
    "SureSelect Focused Exome",
    "Twist_Target_hg19.bed",
    "other",
)


class JobType(StrEnum):
    UPLOAD: str = "upload"
    ANALYSIS: str = "analysis"


class CaseActions(StrEnum):
    ANALYZE: str = "analyze"
    HOLD: str = "hold"
    RUNNING: str = "running"

    @classmethod
    def actions(cls) -> list[str]:
        return list(map(lambda action: action.value, cls))


CONTAINER_OPTIONS = ("Tube", "96 well plate", "No container")


class ControlOptions(StrEnum):
    NEGATIVE: str = "negative"
    POSITIVE: str = "positive"
    EMPTY: str = ""


DEFAULT_CAPTURE_KIT = "twistexomecomprehensive_10.2_hg19_design.bed"


class CustomerId(StrEnum):
    CG_INTERNAL_CUSTOMER: str = "cust000"
    CUST001: str = "cust001"
    CUST002: str = "cust002"
    CUST003: str = "cust003"
    CUST004: str = "cust004"
    CUST032: str = "cust032"
    CUST042: str = "cust042"
    CUST110: str = "cust110"
    CUST127: str = "cust127"
    CUST132: str = "cust132"
    CUST143: str = "cust143"
    CUST147: str = "cust147"
    CUST999: str = "cust999"


class SequencingRunDataAvailability(StrEnum):
    ON_DISK: str = "ondisk"
    REMOVED: str = "removed"
    REQUESTED: str = "requested"
    PROCESSING: str = "processing"
    RETRIEVED: str = "retrieved"

    @classmethod
    def statuses(cls) -> list[str]:
        return list(map(lambda status: status.value, cls))


class AnalysisType(StrEnum):
    TARGETED_GENOME_SEQUENCING: str = "tgs"
    WHOLE_EXOME_SEQUENCING: str = "wes"
    WHOLE_GENOME_SEQUENCING: str = "wgs"
    WHOLE_TRANSCRIPTOME_SEQUENCING: str = "wts"
    OTHER: str = "other"


class CancerAnalysisType(StrEnum):
    TUMOR_NORMAL = auto()
    TUMOR_NORMAL_PANEL = auto()
    TUMOR_NORMAL_WGS = auto()
    TUMOR_PANEL = auto()
    TUMOR_WGS = auto()


class PrepCategory(StrEnum):
    COVID: str = "cov"
    MICROBIAL: str = "mic"
    READY_MADE_LIBRARY: str = "rml"
    TARGETED_GENOME_SEQUENCING: str = "tgs"
    WHOLE_EXOME_SEQUENCING: str = "wes"
    WHOLE_GENOME_SEQUENCING: str = "wgs"
    WHOLE_TRANSCRIPTOME_SEQUENCING: str = "wts"


class SexOptions(StrEnum):
    MALE: str = "male"
    FEMALE: str = "female"
    UNKNOWN: str = "unknown"


SARS_COV_REGEX = "^[0-9]{2}CS[0-9]{6}$"

STATUS_OPTIONS = ("affected", "unaffected", "unknown")


class StatusOptions(StrEnum):
    AFFECTED: str = "affected"
    UNAFFECTED: str = "unaffected"
    UNKNOWN: str = "unknown"


class Workflow(StrEnum):
    BALSAMIC: str = "balsamic"
    BALSAMIC_PON: str = "balsamic-pon"
    BALSAMIC_QC: str = "balsamic-qc"
    BALSAMIC_UMI: str = "balsamic-umi"
    DEMULTIPLEX: str = "demultiplex"
    FLUFFY: str = "fluffy"
    JASEN: str = "jasen"
    MICROSALT: str = "microsalt"
    MIP_DNA: str = "mip-dna"
    MIP_RNA: str = "mip-rna"
    MUTANT: str = "mutant"
    RAREDISEASE: str = "raredisease"
    RAW_DATA: str = "raw-data"
    RNAFUSION: str = "rnafusion"
    RSYNC: str = "rsync"
    SPRING: str = "spring"
    TAXPROFILER: str = "taxprofiler"
    TOMTE: str = "tomte"


class FileFormat(StrEnum):
    CSV: str = "csv"
    FASTQ: str = "fastq"
    JSON: str = "json"
    PNG: str = "png"
    TSV: str = "tsv"
    TXT: str = "txt"
    XML: str = "xml"
    YAML: str = "yaml"


class GenomeVersion(StrEnum):
    GRCh37: str = "GRCh37"
    GRCh38: str = "GRCh38"
    T2T_CHM13: str = "T2T-CHM13v2.0"
    CANFAM3 = auto()
    HG19: str = "hg19"
    HG38: str = "hg38"


class SampleType(StrEnum):
    TUMOR: str = "tumor"
    NORMAL: str = "normal"


class DataDelivery(StrEnum):
    ANALYSIS_FILES: str = "analysis"
    ANALYSIS_SCOUT: str = "analysis-scout"
    BAM: str = "bam"
    FASTQ: str = "fastq"
    FASTQ_SCOUT: str = "fastq-scout"
    FASTQ_QC: str = "fastq_qc"
    FASTQ_ANALYSIS: str = "fastq-analysis"
    FASTQ_QC_ANALYSIS: str = "fastq_qc-analysis"
    FASTQ_ANALYSIS_SCOUT: str = "fastq-analysis-scout"
    NIPT_VIEWER: str = "nipt-viewer"
    NO_DELIVERY: str = "no-delivery"
    SCOUT: str = "scout"
    STATINA: str = "statina"


class HastaSlurmPartitions(StrEnum):
    DRAGEN: str = "dragen"


class FileExtensions(StrEnum):
    BAM: str = ".bam"
    BCF: str = ".bcf"
    BED: str = ".bed"
    COMPLETE: str = ".complete"
    CONFIG: str = ".config"
    CRAM: str = ".cram"
    CSV: str = ".csv"
    FASTQ: str = ".fastq"
    FASTQ_GZ: str = ".fastq.gz"
    GPG: str = ".gpg"
    GZIP: str = ".gz"
    HTML: str = ".html"
    JSON: str = ".json"
    KEY: str = ".key"
    LOG: str = ".log"
    MD5: str = ".md5"
    MD5SUM: str = ".md5sum"
    NO_EXTENSION: str = ""
    PASS_PHRASE: str = ".passphrase"
    PENDING: str = ".pending"
    PNG: str = ".png"
    SBATCH: str = ".sbatch"
    SPRING: str = ".spring"
    SH: str = ".sh"
    TAR: str = ".tar"
    TMP: str = ".tmp"
    TSV: str = ".tsv"
    TXT: str = ".txt"
    VCF: str = ".vcf"
    VCF_GZ: str = ".vcf.gz"
    XLSX: str = ".xlsx"
    XML: str = ".xml"
    YAML: str = ".yaml"


class APIMethods(StrEnum):
    POST: str = "POST"
    PUT: str = "PUT"
    GET: str = "GET"
    DELETE: str = "DELETE"
    PATCH: str = "PATCH"


class MicrosaltQC:
    AVERAGE_COVERAGE_THRESHOLD: int = 10
    MWX_THRESHOLD_SAMPLES_PASSING: float = 0.9
    COVERAGE_10X_THRESHOLD: float = 0.75
    DUPLICATION_RATE_THRESHOLD: float = 0.8
    INSERT_SIZE_THRESHOLD: int = 100
    MAPPED_RATE_THRESHOLD: float = 0.3
    NEGATIVE_CONTROL_READS_THRESHOLD: float = 0.2
    TARGET_READS: int = 6000000
    TARGET_READS_FAIL_THRESHOLD: float = 0.7


class MicrosaltAppTags(StrEnum):
    MWRNXTR003: str = "MWRNXTR003"
    MWXNXTR003: str = "MWXNXTR003"
    VWGNXTR001: str = "VWGNXTR001"
    PREP_CATEGORY: str = "mic"


class MutantQC:
    EXTERNAL_NEGATIVE_CONTROL_READS_THRESHOLD: int = 100000
    INTERNAL_NEGATIVE_CONTROL_READS_THRESHOLD: int = 2000
    FRACTION_OF_SAMPLES_WITH_FAILED_QC_THRESHOLD: float = 0.2
    QUALITY_REPORT_FILE_NAME: str = f"QC_report{FileExtensions.JSON}"


DRY_RUN_MESSAGE = "Dry run: process call will not be executed!"


class MetaApis:
    ANALYSIS_API: str = "analysis_api"


class WorkflowManager(StrEnum):
    Slurm: str = "slurm"
    Tower: str = "nf_tower"


class Strandedness(StrEnum):
    """Strandedness types."""

    FORWARD: str = "forward"
    REVERSE: str = "reverse"
    UNSTRANDED: str = "unstranded"


class ReadDirection(IntEnum):
    """Read direction types."""

    FORWARD: int = 1
    REVERSE: int = 2


PIPELINES_USING_PARTIAL_ANALYSES: list[Workflow] = [Workflow.MICROSALT, Workflow.MUTANT]


class MultiQC(StrEnum):
    """MultiQC constants"""

    MULTIQC: str = "multiqc"
    MULTIQC_DATA: str = "multiqc_data"


NG_UL_SUFFIX: str = " ng/uL"


class SequencingQCStatus(Enum):
    FAILED = auto()
    PASSED = auto()
    PENDING = auto()
