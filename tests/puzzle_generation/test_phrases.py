from unittest.mock import patch, mock_open

import pytest

from glassdolls.puzzle_generation.phrases import get_phrase_list
from glassdolls.constants import DATA_RANDOM_PHRASE_EN_XML


@pytest.fixture()
def test_xml_data() -> str:
    return """<?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE phrases [
        <!ELEMENT phrases (phrase*)>

        <!ELEMENT phrase (#PCDATA)>
        <!ATTLIST phrase lang CDATA "en">
        <!ATTLIST phrase src CDATA #IMPLIED>
    ]>
    <phrases>
        <phrase lang="en" src="https://www.gutenberg.org/cache/epub/84/pg84-images.html">Hello, this is a fake XML file.</phrase>
        <phrase lang="en" src="https://www.gutenberg.org/cache/epub/85/pg85-images.html">A second phrase!</phrase>
    </phrases>
    """


@pytest.fixture()
def test_xml_data_phrases() -> list[str]:
    return ["HELLO, THIS IS A FAKE XML FILE.", "A SECOND PHRASE!"]


def test_get_phrase_list_outputs_correctly(
    test_xml_data: str, test_xml_data_phrases: list[str]
) -> None:

    with patch("builtins.open", mock_open(read_data=test_xml_data)) as mock_file:
        phrases = get_phrase_list()

    assert phrases == test_xml_data_phrases
    mock_file.assert_called_with(DATA_RANDOM_PHRASE_EN_XML, "r", encoding="utf-8")
