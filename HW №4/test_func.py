import pytest
from func import assembler

def test_move():
    # Тест move (A=17, B=62, C=3)
    bytes = assembler([("move", 62, 3)])
    assert list(bytes) == [0xD1, 0x87, 0x01]

def test_read():
    # Тест read (A=3, B=103, C=101, D=76)
    bytes = assembler([("read", 103, 101, 76)])
    assert list(bytes) == [0xE3, 0x5C, 0x06, 0x30, 0x01]

def test_write():
    # Тест write (A=1, B=61, C=52, D=812)
    bytes = assembler([("write", 61, 52, 812)])
    assert list(bytes) == [0xA1, 0x47, 0x63, 0x19, 0x00]

def test_bitwise_rotate_right():
    # Тест побитового циклического сдвига вправо (A=20, B=852, C=103)
    bytes = assembler([("bitwise_rotate_right", 852, 103)])
    assert list(bytes) == [0x95, 0x6A, 0x00, 0x00, 0x9C, 0x01]

if __name__ == "__main__":
    pytest.main()
