<div align="center">

# 🧪 QA Automation: Python + Playwright + pytest

**Python · pytest · Playwright · requests · GitHub Actions**

[![tests](https://github.com/DonikaVi/qa-automation-python/actions/workflows/tests.yml/badge.svg)](https://github.com/DonikaVi/qa-automation-python/actions/workflows/tests.yml)
![Python](https://img.shields.io/badge/python-3.12-blue)
![pytest](https://img.shields.io/badge/pytest-8-green)
![Playwright](https://img.shields.io/badge/Playwright-UI-45ba4b)

UI and API autotests against public demo applications, built with a Page Object structure,
parametrized data, clean test data handling and CI on every push.

</div>

---

## 📋 Table of contents
- [What is tested](#-what-is-tested)
- [Tech stack](#-tech-stack)
- [Project structure](#-project-structure)
- [Getting started](#-getting-started)
- [Running tests](#-running-tests)
- [Reports](#-reports)
- [CI](#-ci)
- [Design decisions](#-design-decisions)

## ✅ What is tested

| Layer | Target | Scenarios |
|-------|--------|-----------|
| **UI** | [saucedemo.com](https://www.saucedemo.com) | Login (valid + 4 negative cases), product list, sorting by price, cart badge, full checkout |
| **UI (mobile)** | saucedemo.com, Pixel 7 emulation | Mobile viewport, login and add to cart |
| **API** | [jsonplaceholder](https://jsonplaceholder.typicode.com) | List, single item + JSON schema, 404, filtering, POST, response time |
| **API (auth + CRUD)** | [restful-booker](https://restful-booker.herokuapp.com) | Token auth, create / read / update / patch / delete, 403 without token, data cleanup |
| **Availability** | Public web pages | Status code, content type, key text (parametrized) |

Total: **31 tests**, about 10 seconds locally.

## 🛠 Tech stack

- **Python 3.12**, **pytest** (fixtures, parametrize, markers)
- **Playwright** with the `pytest-playwright` plugin for UI tests
- **requests** + **jsonschema** for API tests
- **Allure** for reports
- **GitHub Actions** for CI

## 🗂 Project structure

```
.
├── pages/                    # Page Objects: locators + actions
│   ├── login_page.py
│   ├── inventory_page.py
│   └── cart_page.py
├── tests/
│   ├── ui/                   # browser tests (desktop + mobile)
│   └── api/                  # HTTP tests (CRUD, schema, availability)
├── conftest.py               # base URLs and shared fixtures
├── pytest.ini                # markers and defaults
├── requirements.txt
└── .github/workflows/tests.yml
```

## 🚀 Getting started

```bash
git clone https://github.com/DonikaVi/qa-automation-python.git
cd qa-automation-python

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
```

## ▶️ Running tests

```bash
pytest                    # everything
pytest -m smoke           # quick sanity set
pytest -m api             # API only
pytest -m ui --headed     # UI with a visible browser
pytest -k login           # by name
pytest -n auto            # parallel (needs: pip install pytest-xdist)
```

Base URLs can be overridden with environment variables: `UI_BASE_URL`, `API_BASE_URL`, `BOOKER_URL`.

## 📊 Reports

```bash
pytest --alluredir=allure-results
allure serve allure-results
```

Debugging a failed UI test: `pytest --tracing retain-on-failure`, then
`playwright show-trace test-results/<test>/trace.zip`.

## 🔁 CI

Tests run on every push and pull request (`.github/workflows/tests.yml`):
checkout → set up Python → install dependencies → install Chromium → `pytest` → upload Allure results.

## 🧠 Design decisions

- **Page Object**: locators live in one place, so a UI change means one fix instead of dozens. Assertions stay in tests.
- **No `sleep`**: Playwright auto-waiting and retrying `expect(...)` only.
- **Independent tests**: every test prepares its own data; created bookings are deleted by a fixture (`yield` teardown).
- **Stable locators**: `data-test` attributes first, never long XPath.
- **Markers**: `smoke`, `ui`, `api` for fast, targeted runs.
- **Public demo sites only**: no real credentials in the repo. The demo credentials are published by the sites themselves.
- Parts of the code were written with an AI assistant and reviewed manually.

## 👤 Author

**Viktoriia Donika**, QA Engineer · [LinkedIn](https://www.linkedin.com/in/viktoriiadonika/) · [GitHub](https://github.com/DonikaVi)
