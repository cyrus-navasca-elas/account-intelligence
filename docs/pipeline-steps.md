# Pipeline Steps Summary

## Deps you'll need
- `anthropic` — LLM calls
- `apify-client` — job posting scraper
- Keys in `.env`: `ANTHROPIC_API_KEY`, `APIFY_API_KEY`

## Pipeline steps

| # | Step | Function | Uses | Out |
|---|------|----------|------|-----|
| 1 | Gather signals | `gather_signals(domain, name)` | Apify (jobs), web fetch (site/news) | `list[Signal]` |
| 2 | Infer initiatives | `infer_initiatives(signals)` | Anthropic | `list[Initiative]` |
| 3 | Map capabilities | `map_capabilities(initiatives, cap_map)` | local YAML/list | `list[MappedInitiative]` (matched or flagged) |
| 4 | Synthesize gaps | `synthesize_gaps(mapped)` | Anthropic | `list[Gap]` |
| 5 | Generate questions | `generate_questions(gaps)` | Anthropic | `list[DiscoveryQuestion]` |
| 6 | Pick angle | `pick_angle(gaps)` | Anthropic | `str` |
| 7 | Assemble brief | `assemble_brief(...)` | pure | `ResearchBrief` |

Orchestrator `run_research()` calls 1→7 in order.

## File layout

```
app/
  routers/research.py         # POST /research/companies/{id}
  services/
    research.py               # run_research() orchestrator
    signals.py                # step 1
    initiatives.py            # step 2
    capabilities.py           # step 3
    gaps.py                   # step 4
    questions.py              # step 5
    angle.py                  # step 6
    brief.py                  # step 7
  clients/
    anthropic.py              # LLM wrapper
    apify.py                  # job scraper wrapper
  schemas/research.py         # all pydantic models
  capability_map.yaml         # source of truth (add later)
  config.py                   # keys, env
```

## Schemas (no confidence score)

**Boundary:**
- `ResearchRequest` — `domain, name, notes, force`
- `ResearchBrief` — `status, current_state, initiatives, gaps, discovery_questions, recommended_angle, sources, flags`

**Internal:**
- `Signal` — `type, url, text`
- `Initiative` — `initiative, evidence, source_url`
- `Gap` — `gap, mapped_capability, impact_hypothesis, initiative_ref`
- `DiscoveryQuestion` — `question, stage, gap_ref`

## Build order

1. Skeleton: router + fake `run_research` returns hardcoded `ResearchBrief`. Prove wiring.
2. Add `ANTHROPIC_API_KEY` + `APIFY_API_KEY` to `config.py` + `.env.example`.
3. Wire step 1 real (Apify jobs first, site/news later).
4. Wire step 2 real (Anthropic).
5. Add capability map YAML + step 3.
6. Wire steps 4, 5, 6 (all LLM).
7. Step 7 assembly.
8. Failure path: no signals → `status="failed"`, empty arrays.
