import re

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_ui_index_served():
    r = client.get("/ui/")
    assert r.status_code == 200
    assert r.headers["content-type"].startswith("text/html")
    assert "account intelligence" in r.text.lower()


def test_ui_bare_path_redirects_to_index():
    r = client.get("/ui")
    assert r.status_code in (200, 307)


def test_ui_logo_links_to_elasapp():
    r = client.get("/ui/")
    assert 'href="https://elasapp.com/"' in r.text
    assert 'src="elas-logo.png"' in r.text


def test_ui_brand_name_is_not_inside_the_link():
    r = client.get("/ui/")
    anchor = re.search(r'<a class="brand__link".*?</a>', r.text, re.S)
    assert anchor is not None
    assert "Account Intelligence" not in anchor.group(0)


def test_ui_logo_asset_served():
    r = client.get("/ui/elas-logo.png")
    assert r.status_code == 200
    assert r.headers["content-type"] == "image/png"


def test_spinner_animates_only_while_busy():
    css = client.get("/ui/styles.css").text
    # The base .spinner rule must not carry the animation...
    base = re.search(r"\.spinner \{(.*?)\}", css, re.S).group(1)
    assert "animation" not in base
    # ...it is applied only by the in-flight selectors.
    assert ".timer:not([hidden]) .spinner" in css
    assert '.results[aria-busy="true"] .spinner' in css


def test_hidden_attribute_is_not_overridden_by_display_rules():
    css = client.get("/ui/styles.css").text
    assert "[hidden] { display: none !important; }" in css


def test_ui_has_no_company_id_field():
    r = client.get("/ui/")
    assert 'id="company_id"' not in r.text
    assert "Company ID" not in r.text


def test_ui_generates_a_sequential_demo_company_id():
    js = client.get("/ui/app.js").text
    assert "function nextCompanyId()" in js
    assert '"demo-" + String(n).padStart(4, "0")' in js
    # the id must be minted at submit time, not read from a form field
    assert "const companyId = nextCompanyId();" in js


def test_company_name_is_the_first_field_and_marked_required():
    r = client.get("/ui/")
    labels = re.findall(r'<label class="label" for="(\w+)"', r.text)
    assert labels[0] == "name", f"expected name first, got {labels}"
    assert '<span class="req" aria-hidden="true">*</span>' in r.text
    assert "required</span>" not in r.text
    # the asterisk is decorative, so the input carries the real required state
    assert re.search(r'<input class="input" id="name"[^>]*\brequired\b', r.text, re.S)


def test_required_mark_is_red():
    css = client.get("/ui/styles.css").text
    assert ".req { color: var(--red);" in css


def test_missing_company_name_blocks_submit_client_side():
    js = client.get("/ui/app.js").text
    assert 'const missingName = nameInput.value.trim() === "";' in js
    assert "if (missingName) {" in js
    # the guard must return before the fetch is issued
    assert js.index("if (missingName) {") < js.index('fetch("/research/companies/')


def test_company_name_stays_optional_in_the_api_schema():
    # the front-end guard must not have leaked into the contract
    from app.schemas.research import ResearchRequest

    assert ResearchRequest().name is None


def test_topbar_meta_shows_version_only():
    js = client.get("/ui/app.js").text
    assert '"v" + info.version' in js
    assert "info.service" not in js
