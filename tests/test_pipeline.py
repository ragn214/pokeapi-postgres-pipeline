import pytest
from unittest.mock import Mock, ANY
from src.pipeline import insert_pokemon, validate_pokemon_record


@pytest.fixture
def pokemon_record():
    return {
        'id': 25,
        'name': 'pikachu',
        'height': 4,
        'weight': 60
    }


# FYI - naming convention for test functions: test_<function>_<expected_behaviour>_<condition>
def test_insert_pokemon_returns_true_when_rowcount_is_one(pokemon_record):
    # Arrange: prepare the inputs
    cursor_mock = Mock()
    cursor_mock.rowcount = 1  # Simulate that one row was inserted

    # Act: call insert_pokemon()
    was_inserted = insert_pokemon(cursor_mock, pokemon_record)

    # Assert: check the returned value
    assert was_inserted is True


def test_insert_pokemon_returns_false_when_rowcount_is_zero(pokemon_record):
    # Arrange: prepare the inputs
    cursor_mock = Mock()
    cursor_mock.rowcount = 0  # Simulate that no rows were inserted

    # Act: call insert_pokemon()
    was_inserted = insert_pokemon(cursor_mock, pokemon_record)

    # Assert: check the returned value
    assert was_inserted is False


def test_insert_pokemon_executes_correct_parameters(pokemon_record):
    cursor_mock = Mock()

    insert_pokemon(cursor_mock, pokemon_record)

    cursor_mock.execute.assert_called_once_with(
        ANY, 
        (25, 'pikachu', 4, 60)
    )


def test_validate_pokemon_rejects_missing_weight(pokemon_record):
    record = pokemon_record.copy()
    del record['weight']  # Remove the 'weight' key to simulate a missing field

    with pytest.raises(ValueError, match="Missing required field: weight"):
        validate_pokemon_record(record)