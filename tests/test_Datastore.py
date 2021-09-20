import pytest
import sqlite3
from src.Database import initialize_tables, import_data, query_data

TEST_DB = r'test.db'
TEST_DATA = {
    "tables": [
        {
            "table": "clients",
            "records": [
                {
                    "client_id": 1,
                    "first_name": "John",
                    "last_name": "Dough",
                    "zipcode": 84211,
                    "country": "USA"
                }
            ]
        },
        {
            "table": "orders",
            "records": [
                {
                    "order_id": 343,
                    "client_id": 1,
                    "ordered_on": "2021-02-11"
                }
            ]
        }
    ]
}


@pytest.fixture()
def setup_test_db():
    with sqlite3.connect(TEST_DB) as conn:
        initialize_tables(conn)
        import_data(TEST_DATA, conn)


def test_query_with_valid_date_1(setup_test_db):
    with sqlite3.connect(TEST_DB) as conn:
        r1, r2 = query_data("2025-12-31", conn)
        assert len(r1) > 0
        assert len(r2) == 0


def test_query_with_valid_date_2(setup_test_db):
    with sqlite3.connect(TEST_DB) as conn:
        r1, r2 = query_data("1980-12-31", conn)
        assert len(r1) == 0
        assert len(r2) > 0


def test_query_with_valid_date_3(setup_test_db):
    with sqlite3.connect(TEST_DB) as conn:
        r1, r2 = query_data("2021-02-11", conn)
        assert len(r1) > 0
        assert len(r2) == 0


def test_query_with_valid_date_4(setup_test_db):
    with sqlite3.connect(TEST_DB) as conn:
        r1, r2 = query_data("2021-02-11", conn)
        assert len([item for item in r1 if 'John' in item]) > 0
        assert len([item for item in r1 if 'Dough' in item]) > 0


def test_query_with_invalid_date_1(setup_test_db):
    with sqlite3.connect(TEST_DB) as conn:
        r1, r2 = query_data("0000-00-111", conn)
        assert len(r1) == 0
        assert len(r2) == 0


def test_import(setup_test_db):
    with sqlite3.connect(TEST_DB) as conn:
        import_data(TEST_DATA, conn)
        r1, r2 = query_data("2021-02-11", conn)
        assert len(r1) > 0
        assert len(r2) == 0
