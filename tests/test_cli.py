import pytest
import sqlite3
from click.testing import CliRunner
from src.jnpr import commit, datastore_query, datastore_import, DB_FILE
from src.Database import initialize_tables


@pytest.fixture()
def setup_test_db():
    with sqlite3.connect(DB_FILE) as conn:
        initialize_tables(conn)


def test_cli_commit():
    runner = CliRunner()
    result = runner.invoke(commit, ['octocat/hello-world'])
    assert "date" in result.output
    assert "email" in result.output
    assert "message" in result.output
    assert "sha" in result.output


def test_cli_specific_commit():
    runner = CliRunner()
    result = runner.invoke(commit, ['octocat/hello-world', '-n1', '-fJSON'])

    assert '"date": "2012-03-06T23:06:50Z"' in result.output
    assert '"email": "octocat@nowhere.com"' in result.output
    assert '"sha": "7fd1a60b01f91b314f59955a4e4d4e80d8edf11d"' in result.output
    assert '"message": ' in result.output


def test_cli_datastore_import(setup_test_db):
    runner = CliRunner()
    runner.invoke(datastore_import, ['-f src/db_records.json'])

    result = runner.invoke(datastore_query, ['-d2021-02-09'])
    assert 'John Dough ordered 5 item(s) before or on 2021-02-09' in result.output


def test_cli_query_real_db(setup_test_db):
    runner = CliRunner()
    result = runner.invoke(datastore_query, ['-d2021-02-09'])

    assert 'John Dough ordered 5 item(s) before or on 2021-02-09' in result.output
