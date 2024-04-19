from typing import Generator

import pytest
from pytest_mock import MockerFixture, MockType

from glassdolls.backend.db_clients import MongoDB, PostgresDB
from glassdolls.game_data.data_init import Initializer


@pytest.fixture()
def mock_mongodb_client(mocker: MockerFixture) -> MockType:
    return mocker.create_autospec(MongoDB)


@pytest.fixture()
def mock_pg_client(mocker: MockerFixture) -> MockType:
    return mocker.create_autospec(PostgresDB)


def test_Initializer_populate_phrases_table_runs_without_error(
    mock_pg_client: MockType,
    mock_mongodb_client: MockType,
) -> None:
    test_initializer = Initializer(pg=mock_pg_client, mongodb=mock_mongodb_client)
    test_initializer.populate_phrases_table(phrase_list=["a", "b", "c"])
    mock_mongodb_client.insert_values.assert_called()


def test_Initializer_populate_spells_table_runs_without_error(
    mock_pg_client: MockType,
    mock_mongodb_client: MockType,
) -> None:

    test_initializer = Initializer(pg=mock_pg_client, mongodb=mock_mongodb_client)
    test_initializer.populate_spell_table(
        spell_mapping={"Fire": "RQ KJ", "Ice": "UV ML"}
    )

    mock_pg_client.insert_values.assert_called()


def test_Initializer_runs_without_error(
    mock_mongodb_client: MockType, mock_pg_client: MockType
) -> None:
    test_initializer = Initializer(pg=mock_pg_client, mongodb=mock_mongodb_client)
    test_initializer.initialize_all()

    mock_pg_client.insert_values.assert_called()
    mock_mongodb_client.insert_values.assert_called()
