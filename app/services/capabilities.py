import json
from functools import lru_cache
from pathlib import Path

import yaml
from pydantic import BaseModel

from app.clients.anthropic import call_llm, parse_json
from app.config import settings
from app.schemas.research import Initiative, MappedInitiative


class Capability(BaseModel):
    id: str
    name: str
    does: str
    signals: list[str] = []
    gap_language: str = ""


class NotCapability(BaseModel):
    id: str
    name: str
    note: str = ""
    signals: list[str] = []


class CapabilityMap(BaseModel):
    capabilities: list[Capability]
    not_capabilities: list[NotCapability]


@lru_cache(maxsize=1)
def load_capability_map() -> CapabilityMap:
    path = Path(settings.capability_map_path)
    if not path.exists():
        return CapabilityMap(capabilities=[], not_capabilities=[])
    data = yaml.safe_load(path.read_text()) or {}
    return CapabilityMap(
        capabilities=[Capability(**c) for c in data.get("capabilities", [])],
        not_capabilities=[NotCapability(**n) for n in data.get("not_capabilities", [])],
    )


CAPABILITY_MAPPING_PROMPT = """
You map prospect initiatives to ELAS QC Holdpoint capabilities.

Inputs:
- INITIATIVES: what the prospect is trying to accomplish (with evidence).
- CAPABILITIES: things ELAS actually does. Only these are valid matches.
- NOT_CAPABILITIES: things ELAS does NOT do. If an initiative maps here,
  DO NOT claim a fit. Instead, set unverified_capability to that id.

For EACH initiative, return one object:
{
  "index": <int>,
  "matched_capability": "<capability name>" | null,
  "unverified_capability": "<not_capability id>" | null,
  "match_reason": "<one short sentence, grounded in signals or gap_language>"
}

Rules:
- Never force a match. If nothing in CAPABILITIES fits, matched_capability = null.
- matched_capability and unverified_capability are mutually exclusive.
- Use exact capability `name` string from the list.
- Use exact not_capability `id` string.

Return JSON: {"mapped": [ ... ]}
""".strip()


def map_capabilities(initiatives: list[Initiative]) -> list[MappedInitiative]:
    if not initiatives:
        return []

    cmap = load_capability_map()
    if not cmap.capabilities:
        return [
            MappedInitiative(
                initiative=i,
                matched_capability=None,
                match_reason="capability_map_empty",
            )
            for i in initiatives
        ]

    user = _format(initiatives, cmap)
    raw = call_llm(system=CAPABILITY_MAPPING_PROMPT, user=user)

    try:
        data = parse_json(raw)
        mapped_by_idx = {m["index"]: m for m in data.get("mapped", [])}
    except (json.JSONDecodeError, TypeError, ValueError, KeyError):
        mapped_by_idx = {}

    valid_names = {c.name for c in cmap.capabilities}
    valid_flag_ids = {n.id for n in cmap.not_capabilities}

    result: list[MappedInitiative] = []
    for idx, init in enumerate(initiatives):
        m = mapped_by_idx.get(idx, {})
        matched = m.get("matched_capability")
        flag = m.get("unverified_capability")
        if matched not in valid_names:
            matched = None
        if flag not in valid_flag_ids:
            flag = None
        result.append(
            MappedInitiative(
                initiative=init,
                matched_capability=matched,
                unverified_capability=flag,
                match_reason=m.get("match_reason", ""),
            )
        )
    return result


def detect_flags_from_skills(signals, cmap):
    """Return deterministic 'capability_unverified: <id>' flags from Signal.facts.skills.

    Case-insensitive substring match. Deduped. Ignores signals without JobFacts.
    """
    hits: list[str] = []
    seen: set[str] = set()
    for s in signals:
        if s.type != "job_posting":
            continue
        facts = getattr(s, "facts", None)
        if not facts or not facts.skills:
            continue
        skill_blob = " | ".join(facts.skills).lower()
        for nc in cmap.not_capabilities:
            for token in nc.signals:
                if token.lower() in skill_blob:
                    flag = f"capability_unverified: {nc.id}"
                    if flag not in seen:
                        seen.add(flag)
                        hits.append(flag)
                    break
    return hits


def _format(initiatives: list[Initiative], cmap: CapabilityMap) -> str:
    inits = "\n".join(
        f"[{i}] {init.initiative} — evidence: {init.evidence}"
        for i, init in enumerate(initiatives)
    )
    caps = "\n".join(
        f"- {c.name}: {c.does}"
        + (f" | signals: {', '.join(c.signals)}" if c.signals else "")
        + (f" | gap: {c.gap_language}" if c.gap_language else "")
        for c in cmap.capabilities
    )
    ncaps = "\n".join(
        f"- id={n.id} | {n.name}" + (f" — {n.note}" if n.note else "")
        for n in cmap.not_capabilities
    )
    return (
        f"INITIATIVES:\n{inits}\n\n"
        f"CAPABILITIES:\n{caps}\n\n"
        f"NOT_CAPABILITIES:\n{ncaps}"
    )
