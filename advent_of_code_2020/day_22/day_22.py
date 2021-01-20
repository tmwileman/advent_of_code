from __future__ import annotations

from typing import NamedTuple, Tuple, List
from collections import deque
import itertools

class Game:
    def __init__(self, deck1: List[int], deck2: List[int]) -> None:
        self.deck1 = deque(deck1)
        self.deck2 = deque(deck2)
        self.game_over = False
        
    def play_one(self) -> None:
        card1 = self.deck1.popleft()
        card2 = self.deck2.popleft()
        if card1 > card2:
            self.deck1.extend([card1, card2])
        elif card2 > card1:
            self.deck2.extend([card2, card1])
        else:
            raise RuntimeError("equal cards")
        if not self.deck1 or not self.deck2:
            self.game_over = True

    def play(self) -> None:
        while not self.game_over:
            self.play_one()
    
    def winning_score(self) -> int:
        if not self.game_over:
            raise RuntimeError("game not over")
        winning_hand = self.deck1 or self.deck2
        return sum(card * i for card, i in zip(reversed(winning_hand), itertools.count(1)))

def make_decks(raw: str) -> Tuple[List[int], List[int]]:
    hand1, hand2 = raw.split("\n\n")
    deck1 = [int(line.strip()) for line in hand1.split("\n")[1:]]
    deck2 = [int(line.strip()) for line in hand2.split("\n")[1:]]
    
    return deck1, deck2

class RecursiveGame:
    def __init__(self, deck1: List[int], deck2: List[int]) -> None:
        self.deck1 = deque(deck1)
        self.deck2 = deque(deck2)
        self.winner = None
        self.seen = set()
        
    def signature(self) -> Tuple[Tuple[int], Tuple[int]]:
        return (tuple(self.deck1), tuple(self.deck2))
    
    def play_one(self) -> None:
        sig = self.signature()
        if sig in self.seen:
            self.winner = 1
            return
        else:
            self.seen.add(sig)
        
        card1 = self.deck1.popleft()
        card2 = self.deck2.popleft()
        
        if len(self.deck1) >= card1 and len(self.deck2) >= card2:
            recursive_game = RecursiveGame(
                list(self.deck1)[:card1],
                list(self.deck2)[:card2]
            )
            recursive_game.play()
            winner = recursive_game.winner
        else:
            winner = 1 if card1 > card2 else 2
        
        if winner == 1:
            self.deck1.extend([card1, card2])
        else:
            self.deck2.extend([card2, card1])
        
        if not self.deck1:
            self.winner = 2
            return
        
        if not self.deck2:
            self.winner = 1
            return
        
            
    def play(self) -> None:
        while not self.winner:
            self.play_one()
    
    def winning_score(self) -> int:
        if not self.winner:
            raise RuntimeError("game not over")
        winning_hand = self.deck1 or self.deck2
        return sum(card * i for card, i in zip(reversed(winning_hand), itertools.count(1)))
    
RAW = """Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10"""

DECK1, DECK2 = make_decks(RAW)
GAME = Game(DECK1, DECK2)
GAME.play()
assert GAME.winning_score() == 306

RECURSIVE_GAME = RecursiveGame(DECK1, DECK2)
RECURSIVE_GAME.play()
assert RECURSIVE_GAME.winning_score() == 291

with open('/Users/thomaswileman/advent_of_code/advent_of_code_2020/day_22/input.txt') as f:
    raw = f.read()
    deck1, deck2 = make_decks(raw)
    game = Game(deck1, deck2)
    game.play()
    print(game.winning_score())
    recursive_game = RecursiveGame(deck1, deck2)
    recursive_game.play()
    print(recursive_game.winning_score())