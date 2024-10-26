import pytest
from parser import parse_value, parse_assignment

def test_parse_value():
    assert parse_value('10') == 10
    assert parse_value('(1, 2, 3)') == [1, 2, 3]
    assert parse_value('dict(a=1, b=2)') == {'a': 1, 'b': 2}
    assert parse_value('dict(x=(1, 2), y=dict(a=3))') == {'x': [1, 2], 'y': {'a': 3}}
    
    with pytest.raises(ValueError):
        parse_value('invalid')

def test_parse_assignment():
    assert parse_assignment('def x = 10;') == ('x', 10)
    assert parse_assignment('def my_list = (1, 2, 3);') == ('my_list', [1, 2, 3])
    assert parse_assignment('def my_dict = dict(a=1, b=2);') == ('my_dict', {'a': 1, 'b': 2})

    with pytest.raises(ValueError):
        parse_assignment('def invalid;')
    with pytest.raises(ValueError):
        parse_assignment('not a valid assignment;')

if __name__ == "__main__":
    pytest.main()
