from cg.server.ext import rna_dna_collections_service
from cg.services.delivery_message.messages.delivery_message import DeliveryMessage
from cg.services.delivery_message.messages.utils import (
    get_caesar_delivery_path,
    get_scout_link,
)
from cg.store.models import Case


def get_case_message(case: Case) -> str:

    related_uploaded_dna_cases: list[Case] = (
        rna_dna_collections_service.get_uploaded_related_dna_cases(rna_case=case)
    )
    scout_links: list[str] = [get_scout_link(case) for case in related_uploaded_dna_cases]
    scout_links_row_separated: str = "\n".join(scout_links)

    delivery_path: str = get_caesar_delivery_path(case)
    return (
        f"Hello,\n\n"
        f"The analysis for case {case.name} has been uploaded to the corresponding DNA case(s) on Scout at:\n\n"
        f"{scout_links_row_separated}\n\n"
        f"The analysis files are currently being uploaded to your inbox on Caesar:\n\n"
        f"{delivery_path}"
    )


def get_cases_message(cases: list[Case]) -> str:
    message: str = "Hello,\n\n"
    for case in cases:
        related_uploaded_dna_cases: list[Case] = (
            rna_dna_collections_service.get_uploaded_related_dna_cases(rna_case=case)
        )
        scout_links: list[str] = [get_scout_link(case) for case in related_uploaded_dna_cases]
        scout_links_row_separated: str = "\n".join(scout_links)

        message = (
            message
            + f"The analysis for case {case.name} has been uploaded to the corresponding DNA case(s) on Scout at:\n\n"
            + f"{scout_links_row_separated}\n\n"
        )

    delivery_path: str = get_caesar_delivery_path(cases[0])

    message = (
        message
        + "The fastq and analysis files are currently being uploaded to your inbox on Caesar:\n\n"
        + f"{delivery_path}"
    )

    return message


class RNAFastqAnalysisMessage(DeliveryMessage):
    def create_message(self, cases: list[Case]) -> str:
        if len(cases) == 1:
            return get_case_message(cases[0])
        return get_cases_message(cases)
