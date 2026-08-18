from typing import Literal

from pydantic import BaseModel

SignalType = Literal["job_posting", "news", "site", "award"]
DiscoveryStage = Literal[
    "current_state",
    "current_state_impact",
    "org_strain",
    "root_cause",
    "future_state",
    "gap_question",
]
BriefStatus = Literal["enriched", "failed"]


class ResearchRequest(BaseModel):
    domain: str | None = None
    name: str | None = None
    notes: str | None = None
    force: bool = False


class Signal(BaseModel):
    type: SignalType
    url: str
    text: str


class Initiative(BaseModel):
    initiative: str
    evidence: str
    source_url: str


class MappedInitiative(BaseModel):
    initiative: Initiative
    matched_capability: str | None
    match_reason: str
    unverified_capability: str | None = None


class Gap(BaseModel):
    gap: str
    mapped_capability: str
    impact_hypothesis: str
    initiative_ref: int


class DiscoveryQuestion(BaseModel):
    question: str
    stage: DiscoveryStage
    gap_ref: int


class Source(BaseModel):
    type: str
    url: str
    summary: str


class ResearchBrief(BaseModel):
    status: BriefStatus
    current_state: str
    initiatives: list[Initiative]
    gaps: list[Gap]
    discovery_questions: list[DiscoveryQuestion]
    recommended_angle: str
    sources: list[Source]
    flags: list[str]
