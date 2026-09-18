/* Account Intelligence — thin UI over POST /research/companies/{id} */

const form = document.getElementById("research-form");
const submitBtn = document.getElementById("submit");
const timer = document.getElementById("timer");
const timerText = document.getElementById("timer-text");
const results = document.getElementById("results");
const nameInput = document.getElementById("name");
const nameErr = document.getElementById("name-err");

/* Demo build: the API takes a company id in the path, but this UI does not ask
   for one. Mint a sequential id instead. v0's run_research() never reads the id
   and there is no brief store, so the value has no downstream effect. */
let seqFallback = 0;

function nextCompanyId() {
  const KEY = "ai-demo-company-seq";
  let n;
  try {
    n = parseInt(localStorage.getItem(KEY) || "0", 10) + 1;
    if (!Number.isFinite(n) || n < 1) n = 1;
    localStorage.setItem(KEY, String(n));
  } catch (_) {
    n = (seqFallback += 1); // storage blocked (private window) — count in memory
  }
  return "demo-" + String(n).padStart(4, "0");
}

const STAGE_ORDER = [
  "current_state",
  "current_state_impact",
  "org_strain",
  "root_cause",
  "future_state",
  "gap_question",
];
const STAGE_LABEL = {
  current_state: "Current state",
  current_state_impact: "Impact",
  org_strain: "Org strain",
  root_cause: "Root cause",
  future_state: "Future state",
  gap_question: "Gap",
};
const VERDICT_LABEL = { yes: "Reach out", hold: "Hold", skip: "Skip" };

/* ---- tiny DOM helpers ------------------------------------------------ */
function el(tag, attrs = {}, children = []) {
  const node = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (v === null || v === undefined || v === false) continue;
    if (k === "class") node.className = v;
    else if (k === "text") node.textContent = v;
    else node.setAttribute(k, v === true ? "" : String(v));
  }
  for (const child of [].concat(children)) {
    if (child) node.appendChild(child);
  }
  return node;
}

function row(key, value, quiet) {
  if (!value) return null;
  return el("div", { class: "card__row" }, [
    el("span", { class: "card__key", text: key }),
    el("span", { class: "card__val" + (quiet ? " card__val--quiet" : ""), text: value }),
  ]);
}

function link(url, label) {
  if (!url) return null;
  return el("a", { href: url, target: "_blank", rel: "noopener noreferrer", text: label || url });
}

function block(title, count, body) {
  const head = el("div", { class: "block__head" }, [
    el("h2", { class: "block__title", text: title }),
    count === null ? null : el("span", { class: "block__count", text: String(count) }),
  ]);
  return el("section", { class: "block" }, [head].concat(body));
}

/* jump chip: scrolls to a referenced card and flashes it */
function refChip(targetId, label) {
  const chip = el("button", { class: "chip", type: "button", text: label });
  chip.addEventListener("click", () => {
    const target = document.getElementById(targetId);
    if (!target) return;
    target.scrollIntoView({ behavior: "smooth", block: "center" });
    target.classList.remove("card--flash");
    void target.offsetWidth; // restart the animation
    target.classList.add("card--flash");
  });
  return chip;
}

/* ---- renderers ------------------------------------------------------- */
function renderVerdict(brief) {
  const call = VERDICT_LABEL[brief.reach_out] || brief.reach_out;
  const chips = el("div", { class: "chips" }, [
    el("span", {
      class: "chip " + (brief.status === "enriched" ? "chip--ok" : "chip--warn"),
      text: brief.status,
    }),
  ]);
  for (const flag of brief.flags || []) {
    chips.appendChild(el("span", { class: "chip chip--warn", text: flag }));
  }

  return el("section", { class: "verdict verdict--" + (brief.reach_out || "skip") }, [
    el("div", { class: "verdict__head" }, [
      el("span", { class: "verdict__call", text: call }),
      chips,
    ]),
    el("p", { class: "verdict__reason", text: brief.reach_out_reason || "No reason given." }),
  ]);
}

function renderAngle(brief) {
  const body = brief.recommended_angle
    ? el("p", { class: "angle", text: brief.recommended_angle })
    : el("p", { class: "block__empty", text: "No angle produced." });
  return block("Recommended angle", null, body);
}

function renderCurrentState(brief) {
  const body = brief.current_state
    ? el("p", { class: "block__body", text: brief.current_state })
    : el("p", { class: "block__empty", text: "No current-state summary." });
  return block("Current state", null, body);
}

function renderInitiatives(inits) {
  if (!inits.length) {
    return block("Initiatives", 0, el("p", { class: "block__empty", text: "No initiatives inferred." }));
  }
  const cards = inits.map((it, i) =>
    el("article", { class: "card", id: "init-" + i }, [
      el("div", { class: "card__head" }, [
        el("span", { class: "card__num", text: String(i + 1) }),
        el("h3", { class: "card__title", text: it.initiative }),
      ]),
      row("Evidence", it.evidence),
      el("div", { class: "card__foot" }, [it.source_url ? link(it.source_url, "Source") : null]),
    ])
  );
  return block("Initiatives", inits.length, el("div", { class: "cards" }, cards));
}

function renderGaps(gaps) {
  if (!gaps.length) {
    return block("Gaps", 0, el("p", { class: "block__empty", text: "No gaps synthesized." }));
  }
  const cards = gaps.map((g, i) => {
    const foot = el("div", { class: "card__foot" }, [
      g.mapped_capability
        ? el("span", { class: "chip chip--ok", text: g.mapped_capability })
        : el("span", { class: "chip chip--muted", text: "no capability mapped" }),
    ]);
    if (Number.isInteger(g.initiative_ref)) {
      foot.appendChild(refChip("init-" + g.initiative_ref, "→ Initiative " + (g.initiative_ref + 1)));
    }
    return el("article", { class: "card", id: "gap-" + i }, [
      el("div", { class: "card__head" }, [
        el("span", { class: "card__num", text: String(i + 1) }),
        el("h3", { class: "card__title", text: g.gap }),
      ]),
      row("Impact hypothesis", g.impact_hypothesis),
      foot,
    ]);
  });
  return block("Gaps", gaps.length, el("div", { class: "cards" }, cards));
}

function renderQuestions(questions) {
  if (!questions.length) {
    return block("Discovery questions", 0, el("p", { class: "block__empty", text: "No questions generated." }));
  }
  const sorted = questions
    .map((q, i) => ({ q, i }))
    .sort((a, b) => {
      const sa = STAGE_ORDER.indexOf(a.q.stage);
      const sb = STAGE_ORDER.indexOf(b.q.stage);
      return (sa < 0 ? 99 : sa) - (sb < 0 ? 99 : sb) || a.i - b.i;
    });

  const cards = sorted.map(({ q }) => {
    const foot = el("div", { class: "card__foot" }, [
      el("span", { class: "chip chip--stage", text: STAGE_LABEL[q.stage] || q.stage }),
    ]);
    if (Number.isInteger(q.gap_ref)) {
      foot.appendChild(refChip("gap-" + q.gap_ref, "→ Gap " + (q.gap_ref + 1)));
    }
    return el("article", { class: "card" }, [
      el("h3", { class: "card__title", text: q.question }),
      foot,
    ]);
  });
  return block("Discovery questions", questions.length, el("div", { class: "cards" }, cards));
}

function renderSources(sources) {
  if (!sources.length) {
    return block("Sources", 0, el("p", { class: "block__empty", text: "No sources collected." }));
  }
  const head = el("tr", {}, ["Type", "Summary", "Salary", "Skills", "Link"].map((h) => el("th", { text: h })));
  const body = el("tbody", {}, sources.map((s) =>
    el("tr", {}, [
      el("td", { class: "num", text: s.type || "—" }),
      el("td", { class: "src-summary", text: s.summary || "—" }),
      el("td", { class: "num", text: s.salary_range || "—" }),
      el("td", { text: (s.skills || []).join(", ") || "—" }),
      el("td", {}, [link(s.url, "Open") || document.createTextNode("—")]),
    ])
  ));
  const table = el("div", { class: "table-wrap" }, [
    el("table", {}, [el("thead", {}, [head]), body]),
  ]);
  return block("Sources", sources.length, table);
}

function renderBrief(brief) {
  results.replaceChildren(
    renderVerdict(brief),
    renderAngle(brief),
    renderCurrentState(brief),
    renderInitiatives(brief.initiatives || []),
    renderGaps(brief.gaps || []),
    renderQuestions(brief.discovery_questions || []),
    renderSources(brief.sources || [])
  );
  results.firstElementChild.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

function renderError(title, detail) {
  results.replaceChildren(
    el("div", { class: "state state--error" }, [
      el("h2", { class: "state__title", text: title }),
      detail ? el("pre", { text: detail }) : null,
    ])
  );
}

/* ---- request lifecycle ----------------------------------------------- */
let ticking = null;

function setBusy(busy, startedAt) {
  submitBtn.disabled = busy;
  submitBtn.querySelector(".btn__label").textContent = busy ? "Researching…" : "Run research";
  timer.hidden = !busy;
  results.setAttribute("aria-busy", String(busy));

  clearInterval(ticking);
  if (busy) {
    const tick = () => {
      const secs = Math.round((Date.now() - startedAt) / 1000);
      timerText.textContent = "Working… " + secs + "s";
    };
    tick();
    ticking = setInterval(tick, 1000);
  }
}

function value(id) {
  const raw = document.getElementById(id).value.trim();
  return raw === "" ? null : raw;
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  /* Front-end guard only. The API still treats name as optional
     (ResearchRequest.name is `str | None`); this just stops an empty demo run. */
  const missingName = nameInput.value.trim() === "";
  nameErr.hidden = !missingName;
  nameInput.setAttribute("aria-invalid", String(missingName));
  if (missingName) {
    nameInput.focus();
    return;
  }

  const companyId = nextCompanyId();

  const payload = {
    domain: value("domain"),
    name: value("name"),
    notes: value("notes"),
  };

  const startedAt = Date.now();
  setBusy(true, startedAt);
  results.replaceChildren(
    el("div", { class: "state" }, [
      el("span", { class: "spinner" }),
      el("h2", { class: "state__title", text: "Running the pipeline" }),
      el("p", {
        class: "state__body",
        text: "Gathering signals, inferring initiatives, mapping capabilities, synthesizing gaps.",
      }),
    ])
  );

  try {
    const res = await fetch("/research/companies/" + encodeURIComponent(companyId), {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const raw = await res.text();
    if (!res.ok) {
      renderError("Request failed — HTTP " + res.status, raw || res.statusText);
      return;
    }
    renderBrief(JSON.parse(raw));
  } catch (err) {
    renderError("Could not reach the API", String(err && err.message ? err.message : err));
  } finally {
    setBusy(false);
  }
});

/* clear the required-field error as soon as the user types something usable */
nameInput.addEventListener("input", () => {
  if (nameInput.value.trim() !== "") {
    nameErr.hidden = true;
    nameInput.setAttribute("aria-invalid", "false");
  }
});

/* footer meta: which service/version the UI is talking to */
fetch("/version")
  .then((r) => (r.ok ? r.json() : null))
  .then((info) => {
    if (info) document.getElementById("api-meta").textContent = "v" + info.version;
  })
  .catch(() => {});
