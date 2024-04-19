from typing import Generator
from unittest.mock import MagicMock, patch

import pytest
from pytest_mock import MockerFixture, MockType

from glassdolls.backend.db_clients import MongoDB


@patch("glassdolls.backend.db_clients.MongoClient")
def test_MongoDB_connect_runs(mock_mongo: MagicMock) -> None:
    mongodb = MongoDB()
    mongodb.connect()
    assert mongodb.client is not None


@patch("glassdolls.backend.db_clients.MongoClient")
def test_MongoDB_insert_values_runs(mock_mongo: MagicMock) -> None:
    mongodb = MongoDB()
    mongodb.connect()
    mongodb.insert_values(
        collection="test", values=[{"any": "test", "thing": "test_again"}]
    )


@patch("glassdolls.backend.db_clients.MongoClient")
def test_MongoDB_insert_values_errors_if_not_connected(mock_mongo: MagicMock) -> None:
    mongodb = MongoDB()
    with pytest.raises(ConnectionError):
        mongodb.insert_values(
            collection="test", values=[{"any": "test", "thing": "test_again"}]
        )


@patch("glassdolls.backend.db_clients.MongoClient")
def test_MongoDB_query_runs(mock_mongo: MagicMock) -> None:
    mongodb = MongoDB()
    mongodb.connect()
    mongodb.query(collection="test", query={"test": "thing"})


@patch("glassdolls.backend.db_clients.MongoClient")
def test_MongoDB_query_errors_if_not_connected(mock_mongo: MagicMock) -> None:
    mongodb = MongoDB()
    with pytest.raises(ConnectionError):
        mongodb.query(collection="test", query={"test": "thing"})


# @pytest.fixture()
# def mock_mongodb_client(mocker: MockerFixture) -> MockType:
#     return mocker.create_autospec(MongoDB)


# @pytest.fixture()
# def mock_pg_client(mocker: MockerFixture) -> MockType:
#     return mocker.create_autospec(PostgresDB)


# def test_Initializer_populate_phrases_table_runs_without_error(
#     mock_pg_client: MockType,
#     mock_mongodb_client: MockType,
# ) -> None:
#     test_initializer = Initializer(pg=mock_pg_client, mongodb=mock_mongodb_client)
#     test_initializer.populate_phrases_table(phrase_list=["a", "b", "c"])
#     mock_mongodb_client.insert_values.assert_called()
