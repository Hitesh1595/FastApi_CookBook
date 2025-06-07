In this chapter we’re going to cover the following recipes:
    • Setting up testing environments
    • Writing and running unit tests
    • Testing API endpoints
    • Handling logging messages
    • Debugging techniques
    • Performance testing for high traffic application

$ pip install pytest pytest-asyncio httpx
$ pip install pytest-cov


As a first check of the environment, we can try to collect the tests. From the   protoapp root after creating pytest.ini file to check

project folder run:
    $ pytest –-collect-only


The recipe has shown how to configure pytest within a FastAPI project with some of the good practices. Feel free to dig deeper into the Pytest official documentation at the links:
    • Pytest configuration: https://docs.pytest.org/en/stable/reference/customize.html
    • Setup PYTHONPATH in Pytest: https://docs.pytest.org/en/7.1.x/explanationpythonpath.html
    • Pytest good practices: https://docs.pytest.org/en/7.1.x/explanation/goodpractices.html


for fixtures

https://docs.pytest.org/en/7.1.x/reference/fixtures.html.


As you already know, all unit tests can be run from the terminal with the command:
    $ pytest

However, a test can be run individually according to the test call syntax:
    $ pytest <test_module>.py::<test_name>

For example, if we want to run the test function test_read_main_client, run:
    $ pytest tests/test_main.py::test_read_main


# want to run only one integration tests
# add this and in pytest.ini file add

# markers =
#     integration: marks tests as integration

# then run pytest -m integration -vv

@pytest.mark.integration to the method



To use it with pytest, if you didn’t install the packages with the requirements.txt, you need
to install pytest-cov package:
$ pip install pytest-cov



$ pytest --cov protoapp tests
$ pytest --cov app      test_folder_name

You will see a table in the output listing the coverage percentage for each module:
Name                   Stmts   Miss  Cover
------------------------------------------
protoapp\database.py      16      0   100%
protoapp\main.py          37      4    89%
protoapp\schemas.py        8      8     0%
------------------------------------------
TOTAL                     61     12    80%


In addition, a file named .coverage has been created. This is a binary file containing data on the
test coverage and that can be used with additional tools to generate reports out of it.
For example, if you run:

$ coverage html --> generate html


It will create a folder htmlcov with an index.html page containing the coverage page and you
can visualize it by opening it with a browser.

