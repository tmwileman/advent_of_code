from __future__ import annotations

from typing import List, Tuple, NamedTuple, Dict, Iterator
import itertools

def handshakes(subject_number: int = 7) -> Iterator[int]:
    value = 1
    while True:
        yield value
        value = (value * subject_number) % 20201227
    return value

def handshake(loop_number: int, subject_number: int = 7) -> int:
    for i, n in enumerate(handshakes(subject_number)):
        if i == loop_number:
            return n
    raise RuntimeError()

def find_loop_number(public_key: int, subject_number: int = 7) -> int:
    for i, n in enumerate(handshakes(subject_number)):
        if n == public_key:
            return i
    raise RuntimeError()

assert find_loop_number(5764801) == 8
assert find_loop_number(17807724) == 11

door_key = 17773298
card_key = 15530095

door_number = find_loop_number(door_key)
card_number = find_loop_number(card_key)

print(handshake(door_number, card_key))
print(handshake(card_number, door_key)) 
    