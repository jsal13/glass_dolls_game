from typing import Generator

import pytest
from pytest_mock import MockerFixture, MockType

from glassdolls.utils.db_clients import MongoDB, PostgresDB
from glassdolls.initialization.data_init import (
    populate_phrases_table,
    populate_spell_table,
)


@pytest.fixture()
def mock_mongodb_client(mocker: MockerFixture) -> MockType:
    return mocker.create_autospec(MongoDB)


@pytest.fixture()
def mock_pg_client(mocker: MockerFixture) -> MockType:
    return mocker.create_autospec(PostgresDB)


def test_populate_phrases_table_runs_without_error(
    mock_mongodb_client: MockType,
) -> None:
    populate_phrases_table(mongodb=mock_mongodb_client, phrase_list=["a", "b", "c"])

    mock_mongodb_client.insert_values.assert_called()


def test_populate_spells_table_runs_without_error(
    mock_pg_client: MockType,
) -> None:
    populate_spell_table(
        pg=mock_pg_client, spell_mapping={"Fire": "RQ KJ", "Ice": "UV ML"}
    )
    mock_pg_client.insert_values.assert_called()
