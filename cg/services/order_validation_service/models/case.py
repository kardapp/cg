from pydantic import BaseModel, ConfigDict, Discriminator, Field, Tag, model_validator
from typing_extensions import Annotated

from cg.constants.priority import PriorityTerms
from cg.models.orders.sample_base import NAME_PATTERN
from cg.services.order_validation_service.models.discriminators import has_internal_id
from cg.services.order_validation_service.models.existing_sample import ExistingSample
from cg.services.order_validation_service.models.sample import Sample

NewSample = Annotated[Sample, Tag("new")]
ExistingSampleType = Annotated[ExistingSample, Tag("existing")]


class Case(BaseModel):
    name: str = Field(pattern=NAME_PATTERN, min_length=2, max_length=128)
    priority: PriorityTerms = PriorityTerms.STANDARD
    samples: list[
        Annotated[
            NewSample | ExistingSampleType,
            Discriminator(has_internal_id),
        ]
    ]

    @property
    def is_new(self) -> bool:
        return True

    @property
    def enumerated_samples(self):
        return enumerate(self.samples)

    @property
    def enumerated_new_samples(self):
        samples: list[tuple[int, Sample]] = []
        for sample_index, sample in self.enumerated_samples:
            if sample.is_new:
                samples.append((sample_index, sample))
        return samples

    @property
    def enumerated_existing_samples(self) -> list[tuple[int, ExistingSample]]:
        samples: list[tuple[int, ExistingSample]] = []
        for sample_index, sample in self.enumerated_samples:
            if not sample.is_new:
                samples.append((sample_index, sample))
        return samples

    def get_sample(self, sample_name: str) -> Sample | None:
        for sample in self.samples:
            if sample.name == sample_name:
                return sample

    @model_validator(mode="before")
    def convert_empty_strings_to_none(cls, data):
        if isinstance(data, dict):
            for key, value in data.items():
                if value == "":
                    data[key] = None
        return data

    model_config = ConfigDict(extra="ignore")
