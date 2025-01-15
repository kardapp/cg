"""Fixtures for orders parsed from JSON files into dictionaries."""

from pathlib import Path

import pytest

from cg.constants.constants import FileFormat
from cg.io.controller import ReadFile
from cg.models.orders.constants import OrderType
from cg.services.order_validation_service.models.order import Order
from cg.services.order_validation_service.workflows.balsamic.models.order import BalsamicOrder
from cg.services.order_validation_service.workflows.fastq.models.order import FastqOrder
from cg.services.order_validation_service.workflows.fluffy.models.order import FluffyOrder
from cg.services.order_validation_service.workflows.metagenome.models.order import MetagenomeOrder
from cg.services.order_validation_service.workflows.microbial_fastq.models.order import (
    MicrobialFastqOrder,
)
from cg.services.order_validation_service.workflows.microsalt.models.order import MicrosaltOrder
from cg.services.order_validation_service.workflows.mip_dna.models.order import MipDnaOrder
from cg.services.order_validation_service.workflows.mip_rna.models.order import MipRnaOrder
from cg.services.order_validation_service.workflows.mutant.models.order import MutantOrder
from cg.services.order_validation_service.workflows.pacbio_long_read.models.order import PacbioOrder
from cg.services.order_validation_service.workflows.rml.models.order import RmlOrder


@pytest.fixture(scope="session")
def balsamic_order_to_submit(cgweb_orders_dir: Path) -> dict:
    """Load an example cancer order."""
    return ReadFile.get_content_from_file(
        file_format=FileFormat.JSON, file_path=Path(cgweb_orders_dir, "balsamic.json")
    )


@pytest.fixture(scope="session")
def fastq_order_to_submit(cgweb_orders_dir) -> dict:
    """Load an example FASTQ order."""
    return ReadFile.get_content_from_file(
        file_format=FileFormat.JSON, file_path=Path(cgweb_orders_dir, "fastq.json")
    )


@pytest.fixture(scope="session")
def fluffy_order_to_submit(cgweb_orders_dir: Path) -> dict:
    """Load an example Fluffy order."""
    return ReadFile.get_content_from_file(
        file_format=FileFormat.JSON, file_path=Path(cgweb_orders_dir, "fluffy.json")
    )


@pytest.fixture(scope="session")
def metagenome_order_to_submit(cgweb_orders_dir: Path) -> dict:
    """Load an example metagenome order."""
    return ReadFile.get_content_from_file(
        file_format=FileFormat.JSON, file_path=Path(cgweb_orders_dir, "metagenome.json")
    )


@pytest.fixture
def microbial_fastq_order_to_submit(cgweb_orders_dir: Path) -> dict:
    """Load an example microbial order."""
    return ReadFile.get_content_from_file(
        file_format=FileFormat.JSON, file_path=Path(cgweb_orders_dir, "microbial_fastq.json")
    )


@pytest.fixture(scope="session")
def microbial_order_to_submit(cgweb_orders_dir: Path) -> dict:
    """Load an example microbial order."""
    return ReadFile.get_content_from_file(
        file_format=FileFormat.JSON, file_path=Path(cgweb_orders_dir, "microsalt.json")
    )


@pytest.fixture(scope="session")
def mip_dna_order_to_submit(cgweb_orders_dir: Path) -> dict:
    """Load an example MIP-DNA order."""
    return ReadFile.get_content_from_file(
        file_format=FileFormat.JSON, file_path=Path(cgweb_orders_dir, "mip.json")
    )


@pytest.fixture(scope="session")
def mip_rna_order_to_submit(cgweb_orders_dir: Path) -> dict:
    """Load an example RNA order."""
    return ReadFile.get_content_from_file(
        file_format=FileFormat.JSON, file_path=Path(cgweb_orders_dir, "mip_rna.json")
    )


@pytest.fixture(scope="session")
def pacbio_order_to_submit(cgweb_orders_dir) -> dict:
    """Load an example PacBio order."""
    return ReadFile.get_content_from_file(
        file_format=FileFormat.JSON, file_path=Path(cgweb_orders_dir, "pacbio.json")
    )


@pytest.fixture(scope="session")
def rml_order_to_submit(cgweb_orders_dir: Path) -> dict:
    """Load an example RML order."""
    return ReadFile.get_content_from_file(
        file_format=FileFormat.JSON, file_path=Path(cgweb_orders_dir, "rml.json")
    )


@pytest.fixture(scope="session")
def rnafusion_order_to_submit(cgweb_orders_dir: Path) -> dict:
    """Load an example RNA order."""
    return ReadFile.get_content_from_file(
        file_format=FileFormat.JSON, file_path=Path(cgweb_orders_dir, "rnafusion.json")
    )


@pytest.fixture(scope="session")
def sarscov2_order_to_submit(cgweb_orders_dir: Path) -> dict:
    """Load an example sarscov2 order."""
    return ReadFile.get_content_from_file(
        file_format=FileFormat.JSON, file_path=Path(cgweb_orders_dir, "sarscov2.json")
    )


@pytest.fixture(scope="session")
def tomte_order_to_submit(cgweb_orders_dir: Path) -> dict:
    """Load an example TOMTE order."""
    return ReadFile.get_content_from_file(
        file_format=FileFormat.JSON, file_path=Path(cgweb_orders_dir, "tomte.json")
    )


@pytest.fixture(scope="session")
def all_orders_to_submit(
    balsamic_order_to_submit: dict,
    fastq_order_to_submit: dict,
    fluffy_order_to_submit: dict,
    metagenome_order_to_submit: dict,
    microbial_order_to_submit: dict,
    microbial_fastq_order_to_submit: dict,
    mip_dna_order_to_submit: dict,
    mip_rna_order_to_submit: dict,
    pacbio_order_to_submit: dict,
    rml_order_to_submit: dict,
    rnafusion_order_to_submit: dict,
    sarscov2_order_to_submit: dict,
) -> dict[OrderType, Order]:
    """Returns a dict of parsed order for each order type."""
    return {
        OrderType.BALSAMIC: BalsamicOrder.model_validate(balsamic_order_to_submit),
        OrderType.FASTQ: FastqOrder.model_validate(fastq_order_to_submit),
        OrderType.FLUFFY: FluffyOrder.model_validate(fluffy_order_to_submit),
        OrderType.METAGENOME: MetagenomeOrder.model_validate(metagenome_order_to_submit),
        OrderType.MICROBIAL_FASTQ: MicrobialFastqOrder.model_validate(
            microbial_fastq_order_to_submit
        ),
        OrderType.MICROSALT: MicrosaltOrder.model_validate(microbial_order_to_submit),
        OrderType.MIP_DNA: MipDnaOrder.model_validate(mip_dna_order_to_submit),
        OrderType.MIP_RNA: MipRnaOrder.model_validate(mip_rna_order_to_submit),
        OrderType.PACBIO_LONG_READ: PacbioOrder.model_validate(pacbio_order_to_submit),
        OrderType.RML: RmlOrder.model_validate(rml_order_to_submit),
        # OrderType.RNAFUSION: RnaFusionOrder.model_validate(rnafusion_order_to_submit),
        OrderType.SARS_COV_2: MutantOrder.model_validate(sarscov2_order_to_submit),
    }
