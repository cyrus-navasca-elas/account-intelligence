from app.clients import apify, web_search
from app.schemas.research import Signal


def gather_signals(domain: str | None, name: str | None) -> list[Signal]:
    """Collect raw materials for LLM interpretation. No LLM reasoning here."""
    signals: list[Signal] = []

    if domain:
        jobs = apify.fetch_job_postings(domain, name)
        for j in jobs:
            text = _build_job_text(j)
            if not text:
                continue
            signals.append(
                Signal(type="job_posting", url=str(j.get("url") or ""), text=text)
            )

    if name:
        web = web_search.search_company_signals(name, domain)
        for w in web:
            signals.append(Signal(type=w["type"], url=w["url"], text=w["content"]))

    return signals


def _build_job_text(j: dict) -> str:
    """Pack the actor's rich ai_* fields around the full JD.

    Order: header line, structured metadata, keywords, responsibilities/requirements,
    then the full description_text. Drops fields silently if absent.
    """
    desc = str(j.get("description_text") or "").strip()
    if not desc:
        return ""

    title = str(j.get("title") or "").strip()
    locations = ", ".join(j.get("locations_derived") or [])
    date_posted = str(j.get("date_posted") or "")

    header_bits = [b for b in [title, locations, date_posted] if b]
    header = " | ".join(header_bits)

    meta_bits: list[str] = []
    salary = _fmt_salary(j)
    if salary:
        meta_bits.append(f"salary={salary}")
    level = j.get("ai_experience_level")
    if level:
        meta_bits.append(f"level={level}")
    arr = j.get("ai_work_arrangement")
    if arr:
        meta_bits.append(f"arrangement={arr}")
    emp = j.get("ai_employment_type")
    if emp:
        meta_bits.append(f"type={','.join(emp) if isinstance(emp, list) else emp}")
    edu = j.get("ai_education")
    if edu:
        meta_bits.append(f"education={','.join(edu) if isinstance(edu, list) else edu}")

    skills = j.get("ai_key_skills") or []
    keywords = j.get("ai_keywords") or []
    responsibilities = str(j.get("ai_core_responsibilities") or "").strip()
    requirements = str(j.get("ai_requirements_summary") or "").strip()

    parts: list[str] = []
    if header:
        parts.append(header)
    if meta_bits:
        parts.append(" | ".join(meta_bits))
    if skills:
        parts.append(f"Skills: {', '.join(skills)}")
    if keywords:
        parts.append(f"Keywords: {', '.join(keywords)}")
    if responsibilities:
        parts.append(f"Responsibilities: {responsibilities}")
    if requirements:
        parts.append(f"Requirements: {requirements}")
    parts.append(desc)

    return "\n\n".join(parts)


def _fmt_salary(j: dict) -> str:
    lo = j.get("ai_salary_min_value")
    hi = j.get("ai_salary_max_value")
    cur = j.get("ai_salary_currency") or ""
    unit = j.get("ai_salary_unit_text") or ""
    if lo is None and hi is None:
        return ""
    if lo is not None and hi is not None:
        return f"{lo}-{hi} {cur} {unit}".strip()
    return f"{lo or hi} {cur} {unit}".strip()
