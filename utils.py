from typing import Optional, Iterable, Any


def to_integer(msg: str) -> Optional[int]:
    try:
        return abs(int(msg))
    except:
        return False


def normalize_message(msg: str) -> str:
    if not to_integer(msg):
        msg = msg.lower()
        if '1' in msg:
            msg = msg.replace('1', 'I')
    return msg


ROMAN_DIGITS = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X']

def enumerate_roman(iterable: Iterable[Any]) -> list[tuple]:
    result = [(index, item) for index, item in zip(ROMAN_DIGITS, iterable)]
    return result
