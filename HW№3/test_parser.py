# test_config_parser.py

import pytest
import json
from main import parse_value, evaluate_expression, parse_assignment

def test_parse_value():
    memory = {
        "var1": 10,
        "var2": 20,
        "str_var": "Hello",
        "array_var": ({"item1", "item2", "item3"}),
        "dict_var": {
            "key1": 1,
            "key2": 2
        }
    }

    # Test integer parsing
    assert parse_value("42", memory) == 42

    # Test string parsing
    assert parse_value('"Hello"', memory) == "Hello"

    # Test variable lookup
    assert parse_value("var1", memory) == 10

    # Test array parsing
    assert parse_value('({ "item1", "item2", "item3" })', memory) == ["item1", "item2", "item3"]

    # Test dictionary parsing
    assert parse_value('dict(key1=var1, key2=var2)', memory) == {"key1": 10, "key2": 20}

def test_evaluate_expression():
    memory = {
        "a": 10,
        "b": 5
    }

    assert evaluate_expression("+", ["a", "b"], memory) == 15
    assert evaluate_expression("-", ["a", "b"], memory) == 5
    assert evaluate_expression("*", ["a", "b"], memory) == 50
    assert evaluate_expression("/", ["a", "b"], memory) == 2
    assert evaluate_expression("max", ["a", "b"], memory) == 10

def test_parse_assignment():
    memory = {}
    
    # Test defining a variable
    key, value = parse_assignment('def test_var = 100;', memory)
    assert key == "test_var"
    assert value == 100
    assert memory["test_var"] == 100

    # Test defining an array
    key, value = parse_assignment('test_array = ({"item1", "item2", "item3"});', memory)
    assert key == "test_array"
    assert value == ["item1", "item2", "item3"]
    assert memory["test_array"] == ["item1", "item2", "item3"]

    # Test defining a dictionary
    key, value = parse_assignment('test_dict = dict(key1=test_var, key2=200);', memory)
    assert key == "test_dict"
    assert value == {"key1": 100, "key2": 200}
    assert memory["test_dict"] == {"key1": 100, "key2": 200}

if __name__ == '__main__':
    pytest.main()
