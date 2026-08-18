# PRD: Account Intelligence Service (headless, CRM-native)

**Owner:** George
**Status:** Draft v1 (for red-line)
**Last updated:** 12 Aug 2026

---

## 1. One-liner

An API-only service that reads company accounts from the ELAS CRM, researches each one (CRM data + live web), reverse-engineers the account's business initiatives from public signals, maps those to where ELAS creates value, and writes a structured, gap-selling-ready sales brief back onto the company record. No UI.

## 2. Background

Today this is a manual analyst workflow. For a target account we:

1. Pull the company and any known context.
2. Mine public signals (job postings are the richest, plus news, awards, and the company site) to infer what the company is actually trying to accomplish.
3. Map those initiatives to real ELAS capabilities to find where they have a gap we can close.
4. Produce gap-selling discovery questions and a recommended outreach angle.

It works, but it does not scale and it lives in one person's head. This service productizes that workflow as a headless enrichment layer inside ELAS so every account in the CRM can carry a fresh, structured intelligence brief that reps act on directly.

## 3. Goals and non-goals

**Goals**
- Enrich any CRM company account with structured account intelligence via API.
- Support both on-demand (single company) and automatic (event-driven) runs.
- Write results back as discrete, queryable fields, not a free-text dump.
- Ground every claim in a cited source and never invent facts about the prospect or about ELAS.

**Non-goals (v1)**
- No user interface. Consumers are the CRM and internal services only.
- Not writing or sending outreach copy (that is a downstream consumer, see Phasing).
- Not a general-purpose web-scraping product.

## 4. Consumers

- The ELAS CRM (reads the enriched fields, triggers auto-runs).
- Internal automations and reps who trigger on-demand runs.
- A future outreach/sequencing consumer that reads the brief to draft messages.

## 5. Data flow

```
CRM company record  ->  Research Service
                          |  1. read CRM fields (name, domain, notes)
                          |  2. gather web signals (job posts, news, site)
                          |  3. infer initiatives + current state
                          |  4. map to ELAS capability map (source of truth)
                          |  5. produce gaps + discovery questions + angle
                          v
                     write structured fields back to the same CRM record
```

## 6. Triggers

**On-demand:** `POST /v1/research/companies/{companyId}` kicks off a run for one account. Returns a job id immediately (async, see section 10).

**Automatic:** the service subscribes to CRM events and self-triggers on:
- `company.created`
- `company.tagged` with a configured tag (e.g. `research:queue`)

Auto-runs are rate-limited and deduped so the same company is not re-researched inside a cooldown window (proposed: 30 days unless forced).

## 7. Inputs (read from the CRM company object)

| Field | Required | Use |
|---|---|---|
| `id` | yes | Record to write back to |
| `name` | yes | Disambiguation and search |
| `domain` / `website` | **yes for good results** | Anchors web research to the right company |
| `location` / `hq` | no | Disambiguation (e.g. Chelsea London vs NY) |
| `notes` / prior activity | no | Extra context to seed the research |

> **Assumption to confirm:** the CRM company object exposes a stable `domain` field. Web research quality drops sharply without it. If it is missing, the service should attempt to resolve a domain from the name and flag low confidence.

## 8. Enrichment pipeline (the methodology, encoded)

1. **Signal gathering.** Query the web for the company's job postings, recent news/awards, and site content. Job postings are weighted highest because they leak internal initiatives.
2. **Initiative inference.** From the signals, infer what the company is trying to accomplish (e.g. "scaling federal QC across a growing NAVFAC portfolio"). Each initiative must carry its supporting evidence and source URL.
3. **Capability mapping.** Compare initiatives against the **ELAS Capability Map** (a maintained source-of-truth list of what ELAS/QC Holdpoint actually does, see section 12). Only real capabilities may be matched. Unmatched-but-relevant needs are recorded as opportunities, not claimed as fits.
4. **Gap synthesis.** For each mapped initiative, produce the current-state inference, the gap, and an impact hypothesis (what the gap likely costs them).
5. **Discovery generation.** Produce gap-selling questions tagged by stage across the full taxonomy: `current_state` (how it works today), `current_state_impact` (what the gap costs), `org_strain` (personal/organizational load), `root_cause` (diagnosed with them), `future_state` (only after the gap is established), and `gap_question` (the one that earns the meeting).
6. **Angle.** A short recommended outreach wedge grounded in the strongest gap.

## 9. Output data model (written back to the company record)

Discrete fields, per your call. Proposed schema:

| Field | Type | Notes |
|---|---|---|
| `ai_research_status` | enum | `pending` / `enriched` / `failed` |
| `ai_research_updated_at` | timestamp | Last successful run |
| `ai_research_confidence` | enum | `low` / `med` / `high` |
| `ai_current_state` | text | How they likely operate today, inferred |
| `ai_initiatives` | array | `{ initiative, evidence, source_url }` |
| `ai_gaps` | array | `{ gap, mapped_capability, impact_hypothesis }` |
| `ai_discovery_questions` | array | `{ question, stage, gap_ref }` |
| `ai_recommended_angle` | text | The outreach wedge |
| `ai_sources` | array | `{ type, url, summary }` for auditability |
| `ai_flags` | array | e.g. `capability_unverified: Three-Phase Control` |

Example write-back payload:

```json
{
  "ai_research_status": "enriched",
  "ai_research_confidence": "high",
  "ai_current_state": "Runs Three-Phase QC manually across NAVFAC jobs; coordination lives in spreadsheets and email.",
  "ai_initiatives": [
    {
      "initiative": "Scaling federal QC across a growing NAVFAC portfolio",
      "evidence": "Hiring a QCM for USACE/NAVFAC Three-Phase Control on $20M+ jobs; recent $146.3M NAVFAC delivery order.",
      "source_url": "https://..."
    }
  ],
  "ai_gaps": [
    {
      "gap": "No single live view of inspection status across parties",
      "mapped_capability": "QC Holdpoint one-live-view + auto-routing",
      "impact_hypothesis": "Idle crews and wasted inspector trips on missed holdpoints"
    }
  ],
  "ai_discovery_questions": [
    { "question": "Walk me through how one inspection moves from ready to sign-off today, and who touches it.", "stage": "current_state", "gap_ref": 0 }
  ],
  "ai_recommended_angle": "Their QCM hire is a headcount fix for a systems problem; position as making that role scalable across multiple federal jobs.",
  "ai_sources": [ { "type": "job_posting", "url": "https://...", "summary": "QCM req, USACE/NAVFAC Three-Phase" } ],
  "ai_flags": []
}
```

## 10. API surface (proposed)

- `GET  /v1/crm/companies` — pull companies, filterable by segment/tag (for batch selection).
- `POST /v1/research/companies/{companyId}` — trigger on-demand run, returns `{ jobId }`.
- `GET  /v1/research/jobs/{jobId}` — poll status/result.
- `POST /v1/webhooks/crm` — receives CRM events for the auto path.
- Write-back happens service-side via the CRM API; no external caller writes fields directly.

**Processing model:** async. Research involves several web calls and can take tens of seconds, too long for a synchronous response. Caller gets a `jobId`; completion is reported by callback webhook or by polling. (Assumption, confirm.)

## 11. Update / re-run behavior

- Re-running **overwrites** the `ai_*` fields with the latest result and bumps `ai_research_updated_at`.
- Prior results are retained in an append-only history log for audit (proposed), so nothing is silently lost.
- A `force=true` flag bypasses the cooldown for on-demand re-runs.

## 12. Guardrails and quality (important)

- **ELAS Capability Map as source of truth.** The service maps initiatives only against a maintained list of real ELAS capabilities. This is what prevents the model from inventing a fit (the "does ELAS actually do Three-Phase Control?" problem from our Absher work). If a capability is unconfirmed, it goes in `ai_flags`, not in `ai_gaps` as a claim.
- **Cited claims only.** Every initiative and signal carries a source URL. No source, no claim.
- **Confidence surfaced.** Low confidence (e.g. no domain, thin signals) is written to the record so reps do not over-trust a weak brief.
- **No fabricated prospect facts.** If the web yields nothing usable, status is `failed` with a reason, not a hallucinated brief.

## 13. Auth and permissions

- Service-to-service auth (internal token / OAuth client credentials).
- Scoped to read/write only company objects and their `ai_*` fields.
- (Assumption, confirm against ELAS CRM auth model.)

## 14. Success metrics

- % of target-segment companies with a fresh (`< N` day) enriched brief.
- Rep adoption: % of enriched accounts where the brief is used in outreach.
- Downstream: reply/meeting rate on enriched vs non-enriched accounts.
- Quality: % of runs flagged low-confidence or failed (want this trending down).

## 15. Open questions (for you)

1. What does the CRM company object actually expose today, and is there a reliable `domain` field?
2. Are custom `ai_*` fields easy to add to the CRM schema, or do we need a linked "intelligence" sub-object?
3. Callback webhook vs polling for job completion, which fits your stack better?
4. Who maintains the ELAS Capability Map, and where does it live?
5. Cooldown default: is 30 days right, or tied to CRM activity instead?

## 16. Phasing

- **v1:** on-demand + auto trigger, structured write-back, guardrails, async jobs.
- **v2:** batch runs over a saved segment; scheduled refresh of stale briefs.
- **v3:** outreach consumer that reads the brief and drafts sequenced messages (feeds Instantly).
