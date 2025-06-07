In this chapter we’re going to cover the following recipes:
    • Setting up testing environments
    • Writing and running unit tests
    • Testing API endpoints
    • Handling logging messages
    • Debugging techniques
    • Performance testing for high traffic application

$ pip install pytest pytest-asyncio httpx


As a first check of the environment, we can try to collect the tests. From the   protoapp root after creating pytest.ini file to check

project folder run:
    $ pytest –-collect-only


The recipe has shown how to configure pytest within a FastAPI project with some of the good practices. Feel free to dig deeper into the Pytest official documentation at the links:
    • Pytest configuration: https://docs.pytest.org/en/stable/reference/customize.html
    • Setup PYTHONPATH in Pytest: https://docs.pytest.org/en/7.1.x/explanationpythonpath.html
    • Pytest good practices: https://docs.pytest.org/en/7.1.x/explanation/goodpractices.html


for fixtures

https://docs.pytest.org/en/7.1.x/reference/fixtures.html.