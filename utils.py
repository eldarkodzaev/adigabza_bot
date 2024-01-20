from typing import Optional


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
