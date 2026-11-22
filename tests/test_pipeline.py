from unittest.mock import Mock, ANY
from src.pipeline import insert_pokemon


# FYI - naming convention for test functions: test_<function>_<expected_behaviour>_<condition>

def test_insert_pokemon_returns_true_when_rowcount_is_one():
    # Arrange: prepare the inputs
    cursor_mock = Mock()
    cursor_mock.rowcount = 1  # Simulate that one row was inserted

    pokemon_record = {
        'id': 25,
        'name': 'pikachu',
        'height': 4,
        'weight': 60
    }

    # Act: call insert_pokemon()
    was_inserted = insert_pokemon(cursor_mock, pokemon_record)

    # Assert: check the returned value
    assert was_inserted is True


def test_insert_pokemon_returns_false_when_rowcount_is_zero():
    # Arrange: prepare the inputs
    cursor_mock = Mock()
    cursor_mock.rowcount = 0  # Simulate that no rows were inserted

    pokemon_record = {
        'id': 25,
        'name': 'pikachu',
        'height': 4,
        'weight': 60
    }

    # Act: call insert_pokemon()
    was_inserted = insert_pokemon(cursor_mock, pokemon_record)

    # Assert: check the returned value
    assert was_inserted is False


def test_insert_pokemon_executes_correct_parameters():
    cursor_mock = Mock()
    pokemon_record = {
        'id': 25,
        'name': 'pikachu',
        'height': 4,
        'weight': 60
    }

    insert_pokemon(cursor_mock, pokemon_record)

    cursor_mock.execute.assert_called_once_with(
        ANY, 
        (25, 'pikachu', 4, 60)
    )
