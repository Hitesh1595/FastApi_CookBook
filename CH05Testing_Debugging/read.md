# Testing in FastAPI with Pytest

This chapter covers the following testing topics:

* Setting up testing environments
* Writing and running unit tests
* Testing API endpoints
* Handling logging messages
* Debugging techniques
* Performance testing for high-traffic applications

---

## Installation

```bash
pip install pytest pytest-asyncio httpx
pip install pytest-cov
```

---

## First Check: Collecting Tests

After creating a `pytest.ini` file in the project root, you can verify your test discovery by running:

```bash
pytest --collect-only
```

---

## Useful Pytest Documentation

* [Pytest Configuration](https://docs.pytest.org/en/stable/reference/customize.html)
* [Setting PYTHONPATH](https://docs.pytest.org/en/7.1.x/explanationpythonpath.html)
* [Good Practices](https://docs.pytest.org/en/7.1.x/explanation/goodpractices.html)
* [Fixtures](https://docs.pytest.org/en/7.1.x/reference/fixtures.html)

---

## Running Tests

Run all unit tests:

```bash
pytest
```

Run a specific test:

```bash
pytest <test_module>.py::<test_function>
```

Example:

```bash
pytest tests/test_main.py::test_read_main
```

---

## Running Only Integration Tests

To mark a test as an integration test, add a marker:

```python
@pytest.mark.integration
```

Then, in your `pytest.ini` file, add:

```ini
[pytest]
markers =
    integration: marks tests as integration
```

Run only integration tests:

```bash
pytest -m integration -vv
```

---

## Code Coverage

If you haven't installed it via `requirements.txt`, install the `pytest-cov` package:

```bash
pip install pytest-cov
```

Run coverage on your tests:

```bash
pytest --cov protoapp tests
# or
pytest --cov app test_folder_name
```

Sample output:

```
Name                  Stmts   Miss  Cover
-----------------------------------------
protoapp/database.py     16      0   100%
protoapp/main.py         37      4    89%
protoapp/schemas.py       8      8     0%
-----------------------------------------
TOTAL                    61     12    80%
```

---

## Generating HTML Coverage Report

To generate an HTML report:

```bash
coverage html
```

This creates a folder `htmlcov` with an `index.html` page. Open it in a browser to visualize the report.
