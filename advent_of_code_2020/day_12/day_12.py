from __future__ import annotations
from typing import NamedTuple
from dataclasses import dataclass

class Action(NamedTuple):
    action: str
    amount: int
    
    @staticmethod
    def parse(raw: str):
        return Action(raw[0], int(raw[1:]))

# Want to mutate x, y, and heading so cant used NamedTuple            
@dataclass
class Ship:
    x: int = 0
    y: int = 0
    heading: int = 0
    
    def move(self, action: Action) -> None:
        if action.action == 'N':
            self.y += action.amount
        elif action.action == 'S':
            self.y -= action.amount
        elif action.action == 'E':
            self.x += action.amount
        elif action.action == 'W':
            self.x -= action.amount
        elif action.action == 'L':
            self.heading = (self.heading + action.amount) % 360
        elif action.action == 'R':
            self.heading = (self.heading - action.amount) % 360
        elif action.action == 'F':
            if self.heading == 0:
                self.x += action.amount
            elif self.heading == 90:
                self.y += action.amount
            elif self.heading == 180:
                self.x -= action.amount
            elif self.heading == 270:
                self.y -= action.amount
            else:
                raise ValueError(f"bad heading {self.heading}")
        else: raise ValueError(f"unknown action {action}")

@dataclass
class ShipAndWaypoint:
    ship_x: int = 0
    ship_y: int = 0
    ship_heading: int = 0
    
    waypoint_x: int = 10
    waypoint_y: int = 1
    
    def move(self, action: Action) -> None:
        if action.action == 'N':
            self.waypoint_y += action.amount
        elif action.action == 'S':
            self.waypoint_y -= action.amount
        elif action.action == 'E':
            self.waypoint_x += action.amount
        elif action.action == 'W':
            self.waypoint_x -= action.amount
        elif action.action == 'L':
            # rotate the waypoint around the ship
            for turn in range(action.amount // 90):
                self.waypoint_x, self.waypoint_y = -self.waypoint_y, self.waypoint_x
        elif action.action == 'R':
            for turn in range(action.amount // 90):
                self.waypoint_x, self.waypoint_y = self.waypoint_y, -self.waypoint_x
        elif action.action == 'F':
            self.ship_x += action.amount * self.waypoint_x
            self.ship_y += action.amount * self.waypoint_y
        else: raise ValueError(f"unknown action {action}")
                    
RAW = """F10
N3
F7
R90
F11"""

ACTIONS = [Action.parse(line) for line in RAW.split("\n")]
SHIP = Ship()

for action in ACTIONS:
    SHIP.move(action)

assert SHIP.x == 17
assert SHIP.y == -8

SAW = ShipAndWaypoint()
for action in ACTIONS:
    SAW.move(action)
    
assert SAW.ship_x == 214
assert SAW.ship_y == -72



with open('/Users/thomaswileman/advent_of_code/advent_of_code_2020/day_12/input.txt') as f:
    raw = f.read()
    actions = [Action.parse(line) for line in raw.split("\n")]
    ship = Ship()
    saw = ShipAndWaypoint()
    for action in actions:
        ship.move(action)
        saw.move(action)
    print(abs(ship.x) + abs(ship.y))
    print(abs(saw.ship_x) + abs(saw.ship_y))
      