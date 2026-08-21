# Absher Construction — Full Research Brief

**Domain:** `absherco.com`  
**Actor:** `fantastic-jobs/career-site-job-listing-api` (limit=25, timeRange=6m)  
**Web search:** Anthropic `web_search_20250305`  
**Status:** `enriched`

---

## Current state (inferred)

> Absher has accumulated ~$357.4M in federal contract awards with DoD as its top agency, and is actively hiring a QC Manager with USACE/NAVFAC experience and a DoD Superintendent requiring 8+ years of experience on $40M+ federal projects, including NAVFAC/USACE work. Absher is hiring a Concrete Project Manager and a Framing & Drywall Project Manager/Estimator specifically for its 'Self Perform Team,' both roles focused on owning execution, labor productivity, and financial performance of in-house scopes. Absher is simultaneously recruiting a K-12 Superintendent and a K-12 Design-Build Project Manager, with roles explicitly requiring experience managing occupied campuses, academic calendar constraints, and ground-up education projects.

---

## Initiatives

### 1. Expanding federal and DoD construction capabilities

- **Evidence:** Absher has accumulated ~$357.4M in federal contract awards with DoD as its top agency, and is actively hiring a QC Manager with USACE/NAVFAC experience and a DoD Superintendent requiring 8+ years of experience on $40M+ federal projects, including NAVFAC/USACE work.
- **Source:** https://job-boards.greenhouse.io/absherconstruction/jobs/4111271009

### 2. Growing self-perform trade capabilities (concrete, framing, drywall)

- **Evidence:** Absher is hiring a Concrete Project Manager and a Framing & Drywall Project Manager/Estimator specifically for its 'Self Perform Team,' both roles focused on owning execution, labor productivity, and financial performance of in-house scopes.
- **Source:** https://job-boards.greenhouse.io/absherconstruction/jobs/4278702009

### 3. Scaling K-12 education construction market share

- **Evidence:** Absher is simultaneously recruiting a K-12 Superintendent and a K-12 Design-Build Project Manager, with roles explicitly requiring experience managing occupied campuses, academic calendar constraints, and ground-up education projects.
- **Source:** https://job-boards.greenhouse.io/absherconstruction/jobs/4332901009

### 4. Expanding preconstruction and estimating capacity for larger pursuits

- **Evidence:** Absher is hiring a Senior Estimator (for $40M–$100M+ projects) and an Estimator II across multiple office locations, with the Senior role explicitly tasked with leading design-build pursuits and mentoring 2–3 junior estimators to scale the team.
- **Source:** https://job-boards.greenhouse.io/absherconstruction/jobs/4222170009

### 5. Embedding VDC/BIM workflows into project delivery

- **Evidence:** Absher is hiring a VDC Engineer to develop construction models, lead trade coordination meetings, and perform clash detection across projects, with the role described as 'bridging design intent and field execution' through model-based workflows.
- **Source:** https://job-boards.greenhouse.io/absherconstruction/jobs/4182442009

---

## Gaps

### 1. No real-time inspection tracking tied to self-perform labor productivity loops

- **Mapped capability:** `Re-inspection auto-routing + tracking`
- **Impact hypothesis:** Without automated re-inspection routing and status visibility, failed inspections on self-perform concrete and framing scopes create untracked rework cycles that erode the labor cost margins these new PM roles are hired specifically to protect.
- **Initiative ref:** 1

### 2. No unified inspection status view across concurrent occupied-campus phased scopes

- **Mapped capability:** `One live view of every inspection`
- **Impact hypothesis:** Managing inspections across multiple active K-12 job sites with academic calendar hard-stops requires instant visibility into inspection bottlenecks — without it, a single delayed inspection in a live school environment can trigger schedule overruns that damage client relationships in a relationship-driven market segment.
- **Initiative ref:** 2

### 3. Inspection data exists outside the BIM/Procore model environment, breaking the design-to-field feedback loop

- **Mapped capability:** `Coexists with Procore + Autodesk Build`
- **Impact hypothesis:** If field inspection outcomes aren't surfaced inside the tools the VDC Engineer uses to bridge design intent and field execution, clash detection and model updates will lag behind actual site conditions, undermining the core value proposition of the role and the workflow investment.
- **Initiative ref:** 4

---

## Discovery questions

### `current_state`

- (gap 0) When a concrete or framing inspection fails today, how does your team currently find out about it, and what happens next to get it back into the queue?
- (gap 1) With multiple K-12 sites running concurrently right now, where does your team go to get a clear picture of inspection status across all of them at once?
- (gap 2) When a field inspection produces an outcome that should affect the model — a failure, a deviation, a condition that doesn't match design intent — how does that information find its way back into Procore or Autodesk Build today?

### `current_state_impact`

- (gap 0) How are those rework cycles being captured right now in terms of labor hours and cost, and what does it look like when one of them slips through without being recorded?
- (gap 1) Can you walk me through what happened the last time an inspection bottleneck on one of these occupied campuses wasn't caught early enough — what did that actually set in motion?
- (gap 2) How often is your VDC Engineer working from model data that doesn't yet reflect what's actually been built or flagged in the field, and what does that typically cause downstream?

### `org_strain`

- (gap 0) These PM roles were brought on specifically to protect labor cost margins — how much of their bandwidth is currently being consumed just trying to manually track where a failed inspection stands in the re-inspection process?
- (gap 1) In a market where your client relationships depend on reliability, how much time are your PMs or superintendents spending each week just piecing together inspection status information across these sites?
- (gap 2) The VDC Engineer role was brought in to tighten the loop between design intent and field execution — how much of that value is being lost when inspection data sits outside the tools they're working in every day?

### `root_cause`

- (gap 0) What's driving the disconnect between when a failed inspection is logged and when the self-perform crew actually gets redirected — is it a handoff issue, a visibility issue, or something else?
- (gap 1) When inspection visibility breaks down across concurrent phased scopes, what's typically at the center of it — is it how status gets communicated, where it lives, who owns it, or a combination?
- (gap 2) What's keeping inspection outcomes from being surfaced directly inside your BIM and Procore environment — is it a process gap, a tool integration gap, or a data ownership issue?

### `future_state`

- (gap 0) If re-inspection status were automatically routed and visible to the right people the moment a failure was recorded, what would change about how your PMs manage labor deployment on those scopes?
- (gap 1) If every inspection across all your active K-12 sites were visible in one place and bottlenecks surfaced automatically, how would that change the way your team responds before an academic calendar hard-stop becomes a real risk?
- (gap 2) If field inspection results were automatically available inside the tools your VDC Engineer uses for clash detection and model updates, what would that enable them to do differently?

### `gap_question`

- (gap 0) Given where your inspection tracking process is today versus what it needs to be to actually protect those self-perform labor margins, how large is that gap, and what is it costing you on a typical job?
- (gap 1) Between what your team can see today and what it actually needs to see to stay ahead of inspection-driven schedule risk on these occupied campuses, how would you describe that gap — and what's the exposure if it doesn't close?
- (gap 2) Given the investment you've made in BIM workflow and the VDC role, how would you characterize the gap between where inspection data lives today and where it needs to live to make that investment actually pay off in the field?

---

## Recommended angle

The strongest gap is the unified inspection status view across concurrent occupied-campus phased scopes.

When you're running multiple active K-12 sites simultaneously against academic calendar hard-stops, a single inspection bottleneck doesn't stay contained — it ripples across a phased schedule where there's no slack to absorb it. The problem isn't just the delay itself; it's that without real-time visibility across all those scopes at once, your PMs are finding out about stalled inspections reactively, after the window to course-correct has already closed. In a segment where your next contract lives or dies on how the last one ended, that lag is exactly the kind of exposure that erodes the client trust you've spent years building.

---

## Flags

- `capability_unverified: three_phase_control`

---

## Sources (29)

### `job_posting` — https://job-boards.greenhouse.io/absherconstruction/jobs/4371213009
- **Salary:** 21-24 USD/HOUR
- **Skills:** Receptionist, Administrative support, Customer service, Organization, Time-management, Microsoft Office, Communication, Data entry, Scheduling, Record keeping

> Office Assistant | Puyallup, Washington, United States | 2026-08-14T22:36:33  salary=21-24 USD HOUR | level=0-2 | arrangement=On-site | type=FULL_TIME | education=high school  Skills: Receptionist, Ad

### `job_posting` — https://job-boards.greenhouse.io/absherconstruction/jobs/4336695009
- **Salary:** 120000-140000 USD/YEAR
- **Skills:** Commercial construction, Leadership, Communication, Interpersonal skills, Technical competency, Site logistics planning, Project management, Supervision, Mentoring, Technology proficiency, Safety management, Scheduling, Material ordering, Cost monitoring, Subcontractor management

> Assistant Superintendent - Commercial Construction | Tacoma, Washington, United States, Washington, United States | 2026-07-28T20:09:27  salary=120000-140000 USD YEAR | level=5-10 | arrangement=On-sit

### `job_posting` — https://job-boards.greenhouse.io/absherconstruction/jobs/4236128009
- **Salary:** 120000-165000 USD/YEAR
- **Skills:** Quality Control Management, Three-Phase Control Process, Definable Features of Work, Federal Construction Standards, Project Management, Subcontractor Oversight, Inspection Documentation, USACE Compliance, Construction Software, Commissioning, Safety Audits, Technical Judgment, Stakeholder Management, Procurement Tracking, Punch List Management, Field Inspections

> Quality Control Manager - Federal Construction | Washington, District of Columbia, United States, Bremerton, Washington, United States, Tacoma, Washington, United States | 2026-07-28T17:15:46  salary=

### `job_posting` — https://job-boards.greenhouse.io/absherconstruction/jobs/4335861009
- **Salary:** 95000-125000 USD/YEAR
- **Skills:** Estimating, Construction management, Quantity take-offs, Bid solicitation, Scope development, Unit pricing, Math skills, Attention to detail, Organization, Communication, Project management, Drawing interpretation, Subcontractor coordination

> Estimator II | Bellevue, Washington, United States, Puyallup, Washington, United States, Wenatchee, Washington, United States | 2026-07-28T15:00:28  salary=95000-125000 USD YEAR | level=2-5 | arrangem

### `job_posting` — https://job-boards.greenhouse.io/absherconstruction/jobs/4333067009
- **Salary:** 120000-150000 USD/YEAR
- **Skills:** Project Management, Commercial Construction, Value Engineering, Design Coordination, Scheduling, Change Order Negotiation, Relationship Building, Procore, Preconstruction Planning, Estimating, Quality Control, Safety Planning

> Project Manager - Commercial Construction | Ephrata, Washington, United States, Wenatchee, Washington, United States | 2026-07-27T21:24:17  salary=120000-150000 USD YEAR | level=5-10 | arrangement=On-

### `job_posting` — https://job-boards.greenhouse.io/absherconstruction/jobs/4333055009
- **Salary:** 80000-110000 USD/YEAR
- **Skills:** Project Planning, Contract Management, Submittals, RFIs, Change Orders, Material Procurement, Budgeting, Compliance, Cost Tracking, Site Safety, Plan Reading, Project Management Tools, Technical Documentation, Communication, Time Management, Accountability

> Project Engineer - Commercial Construction | Ephrata, Washington, United States, Wenatchee, Washington, United States | 2026-07-27T21:15:24  salary=80000-110000 USD YEAR | level=2-5 | arrangement=On-s

### `job_posting` — https://job-boards.greenhouse.io/absherconstruction/jobs/4332901009
- **Salary:** 120000-160000 USD/YEAR
- **Skills:** Field Leadership, Project Planning, CPM Scheduling, Safety Compliance, Budget Monitoring, Procore, Primavera P6, Constructability Reviews, Union Contract Management, K-12 Construction Management

> Superintendent - K-12/Education Construction | Washington, District of Columbia, United States, Ephrata, Washington, United States, Wenatchee, Washington, United States | 2026-07-27T20:17:04  salary=1

### `job_posting` — https://job-boards.greenhouse.io/absherconstruction/jobs/4332897009
- **Salary:** 120000-140000 USD/YEAR
- **Skills:** Commercial Construction, Leadership, Communication, Technical Competency, Job Site Management, Contractor Supervision, Site Logistics Planning, Craft Labor Management, Mentoring, Technology Proficiency, Diversity and Inclusion, Safety Management

> Assistant Superintendent - Commercial Construction | Ephrata, Washington, United States, Wenatchee, Washington, United States | 2026-07-27T20:11:44  salary=120000-140000 USD YEAR | level=5-10 | arrang

### `job_posting` — https://job-boards.greenhouse.io/absherconstruction/jobs/4309555009
- **Salary:** 95000-125000 USD/YEAR
- **Skills:** Financial Reporting, Month-end Close, Work-in-Progress Reporting, Consolidated Financial Statements, Audit Coordination, Fixed Asset Accounting, Inventory Management, Percentage-of-completion Accounting, Construction Accounting, Leadership, Analytical Skills, Internal Controls

> Financial Accounting Manager | Puyallup, Washington, United States | 2026-07-08T18:50:25  salary=95000-125000 USD YEAR | level=5-10 | arrangement=On-site | type=FULL_TIME  Skills: Financial Reporting,

### `job_posting` — https://job-boards.greenhouse.io/absherconstruction/jobs/4111271009
- **Salary:** 120000-160000 USD/YEAR
- **Skills:** Field Leadership, Project Planning, CPM Scheduling, QA/QC, Safety Management, Subcontractor Management, Federal Contracting, Budget Monitoring, Risk Mitigation, Procore, Primavera P6, OSHA 30, First Aid/CPR, Union Agreement Knowledge, Site Security, Documentation

> Superintendent - DoD Construction Experience | Washington, District of Columbia, United States, Bremerton, Washington, United States | 2026-06-10T02:03:02  salary=120000-160000 USD YEAR | level=5-10 |

### `job_posting` — https://job-boards.greenhouse.io/absherconstruction/jobs/4278702009
- **Salary:** 120000-150000 USD/YEAR
- **Skills:** Project Management, Labor Productivity Tracking, Cost Performance Management, Change Management, Scheduling, Quality Control, Risk Planning, Safety Integration, Mentoring, Stakeholder Management, Procore, OSHA 30

> Concrete Project Manager - Self Perform Team | Bellevue, Washington, United States, Puyallup, Washington, United States, Washington, United States | 2026-06-08T21:15:46  salary=120000-150000 USD YEAR 

### `job_posting` — https://job-boards.greenhouse.io/absherconstruction/jobs/4265757009
- **Salary:** 100000-130000 USD/YEAR
- **Skills:** Technical Coordination, Cost Management, Submittals Management, RFI Management, Clash Detection, Design Review, Bid Package Development, Schedule Management, Change Management, Subcontractor Compliance, Quality Control, Budget Tracking, Mentoring, Construction Means and Methods, Plan Interpretation, Project Management Software

> Senior Project Engineer - Commercial Construction | Seattle, Washington, United States, Tacoma, Washington, United States | 2026-05-31T12:49:46  salary=100000-130000 USD YEAR | level=2-5 | arrangement

### `job_posting` — https://job-boards.greenhouse.io/absherconstruction/jobs/4093869009
- **Salary:** 80000-110000 USD/YEAR
- **Skills:** Project Planning, Contract Management, Submittals, RFIs, Change Orders, Material Procurement, Budgeting, Compliance, Design Document Review, Cost Tracking, Site Safety, Time Management, Communication, Plan Reading, Scheduling Tools, Project Management Tools

> Project Engineer - Commercial Construction | Washington, District of Columbia, United States, Seattle, Washington, United States, Tacoma, Washington, United States | 2026-05-18T14:30:48  salary=80000-

### `job_posting` — https://job-boards.greenhouse.io/absherconstruction/jobs/4222170009
- **Salary:** 125000-165000 USD/YEAR
- **Skills:** Construction Estimating, Preconstruction Management, Design-Build, Value Engineering, Risk Analysis, Budgeting, Subcontractor Management, Bid Analysis, Scope Leveling, Cost Tracking, Mentorship, Commercial Construction

> Senior Estimator | Bellevue, Washington, United States, Puyallup, Washington, United States | 2026-04-15T16:43:59  salary=125000-165000 USD YEAR | level=10+ | arrangement=On-site | type=FULL_TIME | ed

### `job_posting` — https://job-boards.greenhouse.io/absherconstruction/jobs/4182442009
- **Salary:** 80000-100000 USD/YEAR
- **Skills:** Revit, Navisworks, AutoCAD, Civil 3D, Clash Detection, Construction Modeling, 4D Visual Scheduling, Trade Coordination, Constructability Review, VDC Workflows, Spatial Thinking, Project Planning

> VDC Engineer | Wenatchee, Washington, United States, Washington, United States | 2026-03-12T20:19:50  salary=80000-100000 USD YEAR | level=2-5 | arrangement=On-site | type=FULL_TIME | education=bachel

### `job_posting` — https://job-boards.greenhouse.io/absherconstruction/jobs/4181435009
- **Salary:** 120000-150000 USD/YEAR
- **Skills:** Estimating, Project Management, Financial Forecasting, Budget Management, Metal Stud Framing, Drywall Installation, Taping, Labor Productivity Tracking, Contract Document Analysis, Change Order Negotiation, Procurement, Constructability Review

> Framing & Drywall Project Manager/Estimator - Self Perform Team | Springdale, Arkansas, United States, Bellevue, Washington, United States, Puyallup, Washington, United States | 2026-03-11T22:11:50  s

### `job_posting` — https://job-boards.greenhouse.io/absherconstruction/jobs/4173713009
- **Salary:** 120000-160000 USD/YEAR
- **Skills:** Field Leadership, Construction Sequencing, Scheduling, Trade Coordination, Project Closeout, Safety Management, CPM Scheduling, Budget Monitoring, Constructability Reviews, Subcontractor Supervision, Procore, Primavera P6

> Superintendent - Commercial Construction | Tacoma, Washington, United States, Washington, United States | 2026-03-11T15:28:49  salary=120000-160000 USD YEAR | level=10+ | arrangement=On-site | type=FU

### `job_posting` — https://job-boards.greenhouse.io/absherconstruction/jobs/4094515009
- **Salary:** 1-100000 USD/YEAR
- **Skills:** Construction Management, Diversity and Inclusion, Workplace Safety, Mentoring, Professional Development

> Hey Absher, Keep Me in Mind For the Future! | Hinsdale, Massachusetts, United States | 2026-03-11T15:28:48  salary=1-100000 USD YEAR | level=0-2 | arrangement=On-site | type=FULL_TIME  Skills: Constru

### `job_posting` — https://job-boards.greenhouse.io/absherconstruction/jobs/4093914009
- **Salary:** 120000-150000 USD/YEAR
- **Skills:** Project Management, Design-Build, Value Engineering, Design Coordination, Scheduling, Change Order Negotiation, Relationship Building, Budget Management, Safety Planning, Quality Control, Procore, Preconstruction Planning

> Project Manager - K-12 Design Build | Seattle, Washington, United States, Tacoma, Washington, United States | 2026-03-11T15:28:47  salary=120000-150000 USD YEAR | level=5-10 | arrangement=On-site | ty

### `site` — https://www.absherco.com/who-we-are/

> Absher Construction was founded in 1940 by R.L. 'Barney' Absher and is regularly recognized as one of Engineering News-Record's Top 400 U.S. Contractors. Today it is a 100% employee-owned company that

### `site` — https://www.absherco.com/absher-to-host-inaugural-sustainability-week-join-us-september-15th-19th/

> As a signatory of the Contractors Commitment since 2022, Absher Construction has worked to integrate sustainability into its business practices. Its inaugural Sustainability Week covered five categori

### `site` — https://www.absherco.com/project/f200-federal-way-link-extension/

> Absher is a subcontractor on the $193 million Sound Transit Link Light Rail Extension project, partnering with Kiewit Infrastructure West Co. on a $2 billion design-build contract. Absher is responsib

### `site` — https://www.absherco.com/subcontracting-opportunities/

> Absher actively sources opportunities for small, women-owned, minority-owned, and veteran-owned businesses, reflecting its community-focused values. The company serves markets including Hospitality, G

### `site` — https://www.absherco.com/project/othello-square-building-c/

> Absher completed a $16.7 million tenant improvement project for Seattle Children's Hospital housing the Odessa Brown Children's Clinic (OBCC). The 55,000 SF clinic provides pediatric services includin

### `news` — https://www.djc.com/news/co/12173044.html

> The City of Everett plans to award a contract to a joint venture of Absher Construction and Stellar J to convert a former industrial wastewater treatment plant near Naval Station Everett into a combin

### `news` — https://kpq.com/tags/absher-construction/

> The Wenatchee City Council authorized a contract with Absher Construction to complete the Wenatchee Convention Center Expansion Project, reflecting the company's growing presence in Central Washington

### `news` — https://primerfp.com/intel/company/absher-construction-co

> Absher Construction Co has accumulated approximately $357.4 million in federal contract awards, with the Department of Defense as its top agency, according to federal procurement records tracked by Pr

### `news` — https://washingtonapex.org/about-apex/sponsorship/absher/

> Absher Construction became 100% employee-owned in 2022 following three generations of family ownership, with the transition designed to preserve the firm's culture and core purpose of building communi

### `news` — https://2030districts.org/seattle/company/absher-construction/

> Absher Construction is an affiliated Professional Member of the Seattle 2030 District, an organization focused on dramatically reducing energy, water, and transportation impacts of buildings in the ur

---

## Raw JSON

```json
{
  "status": "enriched",
  "current_state": "Absher has accumulated ~$357.4M in federal contract awards with DoD as its top agency, and is actively hiring a QC Manager with USACE/NAVFAC experience and a DoD Superintendent requiring 8+ years of experience on $40M+ federal projects, including NAVFAC/USACE work. Absher is hiring a Concrete Project Manager and a Framing & Drywall Project Manager/Estimator specifically for its 'Self Perform Team,' both roles focused on owning execution, labor productivity, and financial performance of in-house scopes. Absher is simultaneously recruiting a K-12 Superintendent and a K-12 Design-Build Project Manager, with roles explicitly requiring experience managing occupied campuses, academic calendar constraints, and ground-up education projects.",
  "initiatives": [
    {
      "initiative": "Expanding federal and DoD construction capabilities",
      "evidence": "Absher has accumulated ~$357.4M in federal contract awards with DoD as its top agency, and is actively hiring a QC Manager with USACE/NAVFAC experience and a DoD Superintendent requiring 8+ years of experience on $40M+ federal projects, including NAVFAC/USACE work.",
      "source_url": "https://job-boards.greenhouse.io/absherconstruction/jobs/4111271009"
    },
    {
      "initiative": "Growing self-perform trade capabilities (concrete, framing, drywall)",
      "evidence": "Absher is hiring a Concrete Project Manager and a Framing & Drywall Project Manager/Estimator specifically for its 'Self Perform Team,' both roles focused on owning execution, labor productivity, and financial performance of in-house scopes.",
      "source_url": "https://job-boards.greenhouse.io/absherconstruction/jobs/4278702009"
    },
    {
      "initiative": "Scaling K-12 education construction market share",
      "evidence": "Absher is simultaneously recruiting a K-12 Superintendent and a K-12 Design-Build Project Manager, with roles explicitly requiring experience managing occupied campuses, academic calendar constraints, and ground-up education projects.",
      "source_url": "https://job-boards.greenhouse.io/absherconstruction/jobs/4332901009"
    },
    {
      "initiative": "Expanding preconstruction and estimating capacity for larger pursuits",
      "evidence": "Absher is hiring a Senior Estimator (for $40M–$100M+ projects) and an Estimator II across multiple office locations, with the Senior role explicitly tasked with leading design-build pursuits and mentoring 2–3 junior estimators to scale the team.",
      "source_url": "https://job-boards.greenhouse.io/absherconstruction/jobs/4222170009"
    },
    {
      "initiative": "Embedding VDC/BIM workflows into project delivery",
      "evidence": "Absher is hiring a VDC Engineer to develop construction models, lead trade coordination meetings, and perform clash detection across projects, with the role described as 'bridging design intent and field execution' through model-based workflows.",
      "source_url": "https://job-boards.greenhouse.io/absherconstruction/jobs/4182442009"
    }
  ],
  "gaps": [
    {
      "gap": "No real-time inspection tracking tied to self-perform labor productivity loops",
      "mapped_capability": "Re-inspection auto-routing + tracking",
      "impact_hypothesis": "Without automated re-inspection routing and status visibility, failed inspections on self-perform concrete and framing scopes create untracked rework cycles that erode the labor cost margins these new PM roles are hired specifically to protect.",
      "initiative_ref": 1
    },
    {
      "gap": "No unified inspection status view across concurrent occupied-campus phased scopes",
      "mapped_capability": "One live view of every inspection",
      "impact_hypothesis": "Managing inspections across multiple active K-12 job sites with academic calendar hard-stops requires instant visibility into inspection bottlenecks — without it, a single delayed inspection in a live school environment can trigger schedule overruns that damage client relationships in a relationship-driven market segment.",
      "initiative_ref": 2
    },
    {
      "gap": "Inspection data exists outside the BIM/Procore model environment, breaking the design-to-field feedback loop",
      "mapped_capability": "Coexists with Procore + Autodesk Build",
      "impact_hypothesis": "If field inspection outcomes aren't surfaced inside the tools the VDC Engineer uses to bridge design intent and field execution, clash detection and model updates will lag behind actual site conditions, undermining the core value proposition of the role and the workflow investment.",
      "initiative_ref": 4
    }
  ],
  "discovery_questions": [
    {
      "question": "When a concrete or framing inspection fails today, how does your team currently find out about it, and what happens next to get it back into the queue?",
      "stage": "current_state",
      "gap_ref": 0
    },
    {
      "question": "How are those rework cycles being captured right now in terms of labor hours and cost, and what does it look like when one of them slips through without being recorded?",
      "stage": "current_state_impact",
      "gap_ref": 0
    },
    {
      "question": "These PM roles were brought on specifically to protect labor cost margins — how much of their bandwidth is currently being consumed just trying to manually track where a failed inspection stands in the re-inspection process?",
      "stage": "org_strain",
      "gap_ref": 0
    },
    {
      "question": "What's driving the disconnect between when a failed inspection is logged and when the self-perform crew actually gets redirected — is it a handoff issue, a visibility issue, or something else?",
      "stage": "root_cause",
      "gap_ref": 0
    },
    {
      "question": "If re-inspection status were automatically routed and visible to the right people the moment a failure was recorded, what would change about how your PMs manage labor deployment on those scopes?",
      "stage": "future_state",
      "gap_ref": 0
    },
    {
      "question": "Given where your inspection tracking process is today versus what it needs to be to actually protect those self-perform labor margins, how large is that gap, and what is it costing you on a typical job?",
      "stage": "gap_question",
      "gap_ref": 0
    },
    {
      "question": "With multiple K-12 sites running concurrently right now, where does your team go to get a clear picture of inspection status across all of them at once?",
      "stage": "current_state",
      "gap_ref": 1
    },
    {
      "question": "Can you walk me through what happened the last time an inspection bottleneck on one of these occupied campuses wasn't caught early enough — what did that actually set in motion?",
      "stage": "current_state_impact",
      "gap_ref": 1
    },
    {
      "question": "In a market where your client relationships depend on reliability, how much time are your PMs or superintendents spending each week just piecing together inspection status information across these sites?",
      "stage": "org_strain",
      "gap_ref": 1
    },
    {
      "question": "When inspection visibility breaks down across concurrent phased scopes, what's typically at the center of it — is it how status gets communicated, where it lives, who owns it, or a combination?",
      "stage": "root_cause",
      "gap_ref": 1
    },
    {
      "question": "If every inspection across all your active K-12 sites were visible in one place and bottlenecks surfaced automatically, how would that change the way your team responds before an academic calendar hard-stop becomes a real risk?",
      "stage": "future_state",
      "gap_ref": 1
    },
    {
      "question": "Between what your team can see today and what it actually needs to see to stay ahead of inspection-driven schedule risk on these occupied campuses, how would you describe that gap — and what's the exposure if it doesn't close?",
      "stage": "gap_question",
      "gap_ref": 1
    },
    {
      "question": "When a field inspection produces an outcome that should affect the model — a failure, a deviation, a condition that doesn't match design intent — how does that information find its way back into Procore or Autodesk Build today?",
      "stage": "current_state",
      "gap_ref": 2
    },
    {
      "question": "How often is your VDC Engineer working from model data that doesn't yet reflect what's actually been built or flagged in the field, and what does that typically cause downstream?",
      "stage": "current_state_impact",
      "gap_ref": 2
    },
    {
      "question": "The VDC Engineer role was brought in to tighten the loop between design intent and field execution — how much of that value is being lost when inspection data sits outside the tools they're working in every day?",
      "stage": "org_strain",
      "gap_ref": 2
    },
    {
      "question": "What's keeping inspection outcomes from being surfaced directly inside your BIM and Procore environment — is it a process gap, a tool integration gap, or a data ownership issue?",
      "stage": "root_cause",
      "gap_ref": 2
    },
    {
      "question": "If field inspection results were automatically available inside the tools your VDC Engineer uses for clash detection and model updates, what would that enable them to do differently?",
      "stage": "future_state",
      "gap_ref": 2
    },
    {
      "question": "Given the investment you've made in BIM workflow and the VDC role, how would you characterize the gap between where inspection data lives today and where it needs to live to make that investment actually pay off in the field?",
      "stage": "gap_question",
      "gap_ref": 2
    }
  ],
  "recommended_angle": "The strongest gap is the unified inspection status view across concurrent occupied-campus phased scopes.\n\nWhen you're running multiple active K-12 sites simultaneously against academic calendar hard-stops, a single inspection bottleneck doesn't stay contained — it ripples across a phased schedule where there's no slack to absorb it. The problem isn't just the delay itself; it's that without real-time visibility across all those scopes at once, your PMs are finding out about stalled inspections reactively, after the window to course-correct has already closed. In a segment where your next contract lives or dies on how the last one ended, that lag is exactly the kind of exposure that erodes the client trust you've spent years building.",
  "sources": [
    {
      "type": "job_posting",
      "url": "https://job-boards.greenhouse.io/absherconstruction/jobs/4371213009",
      "summary": "Office Assistant | Puyallup, Washington, United States | 2026-08-14T22:36:33\n\nsalary=21-24 USD HOUR | level=0-2 | arrangement=On-site | type=FULL_TIME | education=high school\n\nSkills: Receptionist, Ad",
      "salary_range": "21-24 USD/HOUR",
      "skills": [
        "Receptionist",
        "Administrative support",
        "Customer service",
        "Organization",
        "Time-management",
        "Microsoft Office",
        "Communication",
        "Data entry",
        "Scheduling",
        "Record keeping"
      ]
    },
    {
      "type": "job_posting",
      "url": "https://job-boards.greenhouse.io/absherconstruction/jobs/4336695009",
      "summary": "Assistant Superintendent - Commercial Construction | Tacoma, Washington, United States, Washington, United States | 2026-07-28T20:09:27\n\nsalary=120000-140000 USD YEAR | level=5-10 | arrangement=On-sit",
      "salary_range": "120000-140000 USD/YEAR",
      "skills": [
        "Commercial construction",
        "Leadership",
        "Communication",
        "Interpersonal skills",
        "Technical competency",
        "Site logistics planning",
        "Project management",
        "Supervision",
        "Mentoring",
        "Technology proficiency",
        "Safety management",
        "Scheduling",
        "Material ordering",
        "Cost monitoring",
        "Subcontractor management"
      ]
    },
    {
      "type": "job_posting",
      "url": "https://job-boards.greenhouse.io/absherconstruction/jobs/4236128009",
      "summary": "Quality Control Manager - Federal Construction | Washington, District of Columbia, United States, Bremerton, Washington, United States, Tacoma, Washington, United States | 2026-07-28T17:15:46\n\nsalary=",
      "salary_range": "120000-165000 USD/YEAR",
      "skills": [
        "Quality Control Management",
        "Three-Phase Control Process",
        "Definable Features of Work",
        "Federal Construction Standards",
        "Project Management",
        "Subcontractor Oversight",
        "Inspection Documentation",
        "USACE Compliance",
        "Construction Software",
        "Commissioning",
        "Safety Audits",
        "Technical Judgment",
        "Stakeholder Management",
        "Procurement Tracking",
        "Punch List Management",
        "Field Inspections"
      ]
    },
    {
      "type": "job_posting",
      "url": "https://job-boards.greenhouse.io/absherconstruction/jobs/4335861009",
      "summary": "Estimator II | Bellevue, Washington, United States, Puyallup, Washington, United States, Wenatchee, Washington, United States | 2026-07-28T15:00:28\n\nsalary=95000-125000 USD YEAR | level=2-5 | arrangem",
      "salary_range": "95000-125000 USD/YEAR",
      "skills": [
        "Estimating",
        "Construction management",
        "Quantity take-offs",
        "Bid solicitation",
        "Scope development",
        "Unit pricing",
        "Math skills",
        "Attention to detail",
        "Organization",
        "Communication",
        "Project management",
        "Drawing interpretation",
        "Subcontractor coordination"
      ]
    },
    {
      "type": "job_posting",
      "url": "https://job-boards.greenhouse.io/absherconstruction/jobs/4333067009",
      "summary": "Project Manager - Commercial Construction | Ephrata, Washington, United States, Wenatchee, Washington, United States | 2026-07-27T21:24:17\n\nsalary=120000-150000 USD YEAR | level=5-10 | arrangement=On-",
      "salary_range": "120000-150000 USD/YEAR",
      "skills": [
        "Project Management",
        "Commercial Construction",
        "Value Engineering",
        "Design Coordination",
        "Scheduling",
        "Change Order Negotiation",
        "Relationship Building",
        "Procore",
        "Preconstruction Planning",
        "Estimating",
        "Quality Control",
        "Safety Planning"
      ]
    },
    {
      "type": "job_posting",
      "url": "https://job-boards.greenhouse.io/absherconstruction/jobs/4333055009",
      "summary": "Project Engineer - Commercial Construction | Ephrata, Washington, United States, Wenatchee, Washington, United States | 2026-07-27T21:15:24\n\nsalary=80000-110000 USD YEAR | level=2-5 | arrangement=On-s",
      "salary_range": "80000-110000 USD/YEAR",
      "skills": [
        "Project Planning",
        "Contract Management",
        "Submittals",
        "RFIs",
        "Change Orders",
        "Material Procurement",
        "Budgeting",
        "Compliance",
        "Cost Tracking",
        "Site Safety",
        "Plan Reading",
        "Project Management Tools",
        "Technical Documentation",
        "Communication",
        "Time Management",
        "Accountability"
      ]
    },
    {
      "type": "job_posting",
      "url": "https://job-boards.greenhouse.io/absherconstruction/jobs/4332901009",
      "summary": "Superintendent - K-12/Education Construction | Washington, District of Columbia, United States, Ephrata, Washington, United States, Wenatchee, Washington, United States | 2026-07-27T20:17:04\n\nsalary=1",
      "salary_range": "120000-160000 USD/YEAR",
      "skills": [
        "Field Leadership",
        "Project Planning",
        "CPM Scheduling",
        "Safety Compliance",
        "Budget Monitoring",
        "Procore",
        "Primavera P6",
        "Constructability Reviews",
        "Union Contract Management",
        "K-12 Construction Management"
      ]
    },
    {
      "type": "job_posting",
      "url": "https://job-boards.greenhouse.io/absherconstruction/jobs/4332897009",
      "summary": "Assistant Superintendent - Commercial Construction | Ephrata, Washington, United States, Wenatchee, Washington, United States | 2026-07-27T20:11:44\n\nsalary=120000-140000 USD YEAR | level=5-10 | arrang",
      "salary_range": "120000-140000 USD/YEAR",
      "skills": [
        "Commercial Construction",
        "Leadership",
        "Communication",
        "Technical Competency",
        "Job Site Management",
        "Contractor Supervision",
        "Site Logistics Planning",
        "Craft Labor Management",
        "Mentoring",
        "Technology Proficiency",
        "Diversity and Inclusion",
        "Safety Management"
      ]
    },
    {
      "type": "job_posting",
      "url": "https://job-boards.greenhouse.io/absherconstruction/jobs/4309555009",
      "summary": "Financial Accounting Manager | Puyallup, Washington, United States | 2026-07-08T18:50:25\n\nsalary=95000-125000 USD YEAR | level=5-10 | arrangement=On-site | type=FULL_TIME\n\nSkills: Financial Reporting,",
      "salary_range": "95000-125000 USD/YEAR",
      "skills": [
        "Financial Reporting",
        "Month-end Close",
        "Work-in-Progress Reporting",
        "Consolidated Financial Statements",
        "Audit Coordination",
        "Fixed Asset Accounting",
        "Inventory Management",
        "Percentage-of-completion Accounting",
        "Construction Accounting",
        "Leadership",
        "Analytical Skills",
        "Internal Controls"
      ]
    },
    {
      "type": "job_posting",
      "url": "https://job-boards.greenhouse.io/absherconstruction/jobs/4111271009",
      "summary": "Superintendent - DoD Construction Experience | Washington, District of Columbia, United States, Bremerton, Washington, United States | 2026-06-10T02:03:02\n\nsalary=120000-160000 USD YEAR | level=5-10 |",
      "salary_range": "120000-160000 USD/YEAR",
      "skills": [
        "Field Leadership",
        "Project Planning",
        "CPM Scheduling",
        "QA/QC",
        "Safety Management",
        "Subcontractor Management",
        "Federal Contracting",
        "Budget Monitoring",
        "Risk Mitigation",
        "Procore",
        "Primavera P6",
        "OSHA 30",
        "First Aid/CPR",
        "Union Agreement Knowledge",
        "Site Security",
        "Documentation"
      ]
    },
    {
      "type": "job_posting",
      "url": "https://job-boards.greenhouse.io/absherconstruction/jobs/4278702009",
      "summary": "Concrete Project Manager - Self Perform Team | Bellevue, Washington, United States, Puyallup, Washington, United States, Washington, United States | 2026-06-08T21:15:46\n\nsalary=120000-150000 USD YEAR ",
      "salary_range": "120000-150000 USD/YEAR",
      "skills": [
        "Project Management",
        "Labor Productivity Tracking",
        "Cost Performance Management",
        "Change Management",
        "Scheduling",
        "Quality Control",
        "Risk Planning",
        "Safety Integration",
        "Mentoring",
        "Stakeholder Management",
        "Procore",
        "OSHA 30"
      ]
    },
    {
      "type": "job_posting",
      "url": "https://job-boards.greenhouse.io/absherconstruction/jobs/4265757009",
      "summary": "Senior Project Engineer - Commercial Construction | Seattle, Washington, United States, Tacoma, Washington, United States | 2026-05-31T12:49:46\n\nsalary=100000-130000 USD YEAR | level=2-5 | arrangement",
      "salary_range": "100000-130000 USD/YEAR",
      "skills": [
        "Technical Coordination",
        "Cost Management",
        "Submittals Management",
        "RFI Management",
        "Clash Detection",
        "Design Review",
        "Bid Package Development",
        "Schedule Management",
        "Change Management",
        "Subcontractor Compliance",
        "Quality Control",
        "Budget Tracking",
        "Mentoring",
        "Construction Means and Methods",
        "Plan Interpretation",
        "Project Management Software"
      ]
    },
    {
      "type": "job_posting",
      "url": "https://job-boards.greenhouse.io/absherconstruction/jobs/4093869009",
      "summary": "Project Engineer - Commercial Construction | Washington, District of Columbia, United States, Seattle, Washington, United States, Tacoma, Washington, United States | 2026-05-18T14:30:48\n\nsalary=80000-",
      "salary_range": "80000-110000 USD/YEAR",
      "skills": [
        "Project Planning",
        "Contract Management",
        "Submittals",
        "RFIs",
        "Change Orders",
        "Material Procurement",
        "Budgeting",
        "Compliance",
        "Design Document Review",
        "Cost Tracking",
        "Site Safety",
        "Time Management",
        "Communication",
        "Plan Reading",
        "Scheduling Tools",
        "Project Management Tools"
      ]
    },
    {
      "type": "job_posting",
      "url": "https://job-boards.greenhouse.io/absherconstruction/jobs/4222170009",
      "summary": "Senior Estimator | Bellevue, Washington, United States, Puyallup, Washington, United States | 2026-04-15T16:43:59\n\nsalary=125000-165000 USD YEAR | level=10+ | arrangement=On-site | type=FULL_TIME | ed",
      "salary_range": "125000-165000 USD/YEAR",
      "skills": [
        "Construction Estimating",
        "Preconstruction Management",
        "Design-Build",
        "Value Engineering",
        "Risk Analysis",
        "Budgeting",
        "Subcontractor Management",
        "Bid Analysis",
        "Scope Leveling",
        "Cost Tracking",
        "Mentorship",
        "Commercial Construction"
      ]
    },
    {
      "type": "job_posting",
      "url": "https://job-boards.greenhouse.io/absherconstruction/jobs/4182442009",
      "summary": "VDC Engineer | Wenatchee, Washington, United States, Washington, United States | 2026-03-12T20:19:50\n\nsalary=80000-100000 USD YEAR | level=2-5 | arrangement=On-site | type=FULL_TIME | education=bachel",
      "salary_range": "80000-100000 USD/YEAR",
      "skills": [
        "Revit",
        "Navisworks",
        "AutoCAD",
        "Civil 3D",
        "Clash Detection",
        "Construction Modeling",
        "4D Visual Scheduling",
        "Trade Coordination",
        "Constructability Review",
        "VDC Workflows",
        "Spatial Thinking",
        "Project Planning"
      ]
    },
    {
      "type": "job_posting",
      "url": "https://job-boards.greenhouse.io/absherconstruction/jobs/4181435009",
      "summary": "Framing & Drywall Project Manager/Estimator - Self Perform Team | Springdale, Arkansas, United States, Bellevue, Washington, United States, Puyallup, Washington, United States | 2026-03-11T22:11:50\n\ns",
      "salary_range": "120000-150000 USD/YEAR",
      "skills": [
        "Estimating",
        "Project Management",
        "Financial Forecasting",
        "Budget Management",
        "Metal Stud Framing",
        "Drywall Installation",
        "Taping",
        "Labor Productivity Tracking",
        "Contract Document Analysis",
        "Change Order Negotiation",
        "Procurement",
        "Constructability Review"
      ]
    },
    {
      "type": "job_posting",
      "url": "https://job-boards.greenhouse.io/absherconstruction/jobs/4173713009",
      "summary": "Superintendent - Commercial Construction | Tacoma, Washington, United States, Washington, United States | 2026-03-11T15:28:49\n\nsalary=120000-160000 USD YEAR | level=10+ | arrangement=On-site | type=FU",
      "salary_range": "120000-160000 USD/YEAR",
      "skills": [
        "Field Leadership",
        "Construction Sequencing",
        "Scheduling",
        "Trade Coordination",
        "Project Closeout",
        "Safety Management",
        "CPM Scheduling",
        "Budget Monitoring",
        "Constructability Reviews",
        "Subcontractor Supervision",
        "Procore",
        "Primavera P6"
      ]
    },
    {
      "type": "job_posting",
      "url": "https://job-boards.greenhouse.io/absherconstruction/jobs/4094515009",
      "summary": "Hey Absher, Keep Me in Mind For the Future! | Hinsdale, Massachusetts, United States | 2026-03-11T15:28:48\n\nsalary=1-100000 USD YEAR | level=0-2 | arrangement=On-site | type=FULL_TIME\n\nSkills: Constru",
      "salary_range": "1-100000 USD/YEAR",
      "skills": [
        "Construction Management",
        "Diversity and Inclusion",
        "Workplace Safety",
        "Mentoring",
        "Professional Development"
      ]
    },
    {
      "type": "job_posting",
      "url": "https://job-boards.greenhouse.io/absherconstruction/jobs/4093914009",
      "summary": "Project Manager - K-12 Design Build | Seattle, Washington, United States, Tacoma, Washington, United States | 2026-03-11T15:28:47\n\nsalary=120000-150000 USD YEAR | level=5-10 | arrangement=On-site | ty",
      "salary_range": "120000-150000 USD/YEAR",
      "skills": [
        "Project Management",
        "Design-Build",
        "Value Engineering",
        "Design Coordination",
        "Scheduling",
        "Change Order Negotiation",
        "Relationship Building",
        "Budget Management",
        "Safety Planning",
        "Quality Control",
        "Procore",
        "Preconstruction Planning"
      ]
    },
    {
      "type": "site",
      "url": "https://www.absherco.com/who-we-are/",
      "summary": "Absher Construction was founded in 1940 by R.L. 'Barney' Absher and is regularly recognized as one of Engineering News-Record's Top 400 U.S. Contractors. Today it is a 100% employee-owned company that",
      "salary_range": null,
      "skills": []
    },
    {
      "type": "site",
      "url": "https://www.absherco.com/absher-to-host-inaugural-sustainability-week-join-us-september-15th-19th/",
      "summary": "As a signatory of the Contractors Commitment since 2022, Absher Construction has worked to integrate sustainability into its business practices. Its inaugural Sustainability Week covered five categori",
      "salary_range": null,
      "skills": []
    },
    {
      "type": "site",
      "url": "https://www.absherco.com/project/f200-federal-way-link-extension/",
      "summary": "Absher is a subcontractor on the $193 million Sound Transit Link Light Rail Extension project, partnering with Kiewit Infrastructure West Co. on a $2 billion design-build contract. Absher is responsib",
      "salary_range": null,
      "skills": []
    },
    {
      "type": "site",
      "url": "https://www.absherco.com/subcontracting-opportunities/",
      "summary": "Absher actively sources opportunities for small, women-owned, minority-owned, and veteran-owned businesses, reflecting its community-focused values. The company serves markets including Hospitality, G",
      "salary_range": null,
      "skills": []
    },
    {
      "type": "site",
      "url": "https://www.absherco.com/project/othello-square-building-c/",
      "summary": "Absher completed a $16.7 million tenant improvement project for Seattle Children's Hospital housing the Odessa Brown Children's Clinic (OBCC). The 55,000 SF clinic provides pediatric services includin",
      "salary_range": null,
      "skills": []
    },
    {
      "type": "news",
      "url": "https://www.djc.com/news/co/12173044.html",
      "summary": "The City of Everett plans to award a contract to a joint venture of Absher Construction and Stellar J to convert a former industrial wastewater treatment plant near Naval Station Everett into a combin",
      "salary_range": null,
      "skills": []
    },
    {
      "type": "news",
      "url": "https://kpq.com/tags/absher-construction/",
      "summary": "The Wenatchee City Council authorized a contract with Absher Construction to complete the Wenatchee Convention Center Expansion Project, reflecting the company's growing presence in Central Washington",
      "salary_range": null,
      "skills": []
    },
    {
      "type": "news",
      "url": "https://primerfp.com/intel/company/absher-construction-co",
      "summary": "Absher Construction Co has accumulated approximately $357.4 million in federal contract awards, with the Department of Defense as its top agency, according to federal procurement records tracked by Pr",
      "salary_range": null,
      "skills": []
    },
    {
      "type": "news",
      "url": "https://washingtonapex.org/about-apex/sponsorship/absher/",
      "summary": "Absher Construction became 100% employee-owned in 2022 following three generations of family ownership, with the transition designed to preserve the firm's culture and core purpose of building communi",
      "salary_range": null,
      "skills": []
    },
    {
      "type": "news",
      "url": "https://2030districts.org/seattle/company/absher-construction/",
      "summary": "Absher Construction is an affiliated Professional Member of the Seattle 2030 District, an organization focused on dramatically reducing energy, water, and transportation impacts of buildings in the ur",
      "salary_range": null,
      "skills": []
    }
  ],
  "flags": [
    "capability_unverified: three_phase_control"
  ]
}
```
