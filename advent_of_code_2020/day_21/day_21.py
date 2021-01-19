from __future__ import annotations

from typing import NamedTuple, Set, List, Dict
from collections import defaultdict

class Food(NamedTuple):
    ingredients: List[str]
    allergens: List[str]
    
    @staticmethod
    def parse(line: str) -> Food:
        parts = line.split("(contains ")
        if len(parts) == 1:
            allergens = []
        else:
            allergens = parts[1][:-1].split(", ")
        return Food(parts[0].split(), allergens)
    
def candidates(foods: List[Food]) -> Dict[str, Set[str]]:
    candidates: Dict[str, Set[str]] = {}

    for food in foods:
        for allergen in food.allergens:
            if allergen not in candidates:
                candidates[allergen] = set(food.ingredients)
            else:
                candidates[allergen] = candidates[allergen] & set(food.ingredients)

    allergens = list(candidates)
    
    keep_going = True
    
    while keep_going:
        keep_going = False
        
        known = {allergen: cands for allergen, cands in candidates.items()
                 if len(cands) == 1}
        taken_ingredients = {ingredient for cands in known.values() for ingredient in cands}

        for allergen in allergens:
            if allergen not in known and (candidates[allergen] & taken_ingredients):
                keep_going = True
                candidates[allergen] = candidates[allergen] - taken_ingredients

    return candidates 

def count_no_allergens(foods: List[Food]) -> int:
    cands = candidates(foods)
    can_contain = {ingredient for cands in cands.values() for ingredient in cands}

    return sum(ingredient not in can_contain
                for food in foods
                for ingredient in food.ingredients)

def arrange(candidates: Dict[str, Set[str]]) -> str:
    assert all(len(s) == 1 for s in candidates.values())
    
    return ",".join(next(iter(cands)) for allergen, cands in sorted(candidates.items()))

RAW = """mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)"""

FOODS = [Food.parse(line) for line in RAW.split("\n")]
CANDIDATES = candidates(FOODS)
COUNT = count_no_allergens(FOODS)
ARRANGED = arrange(CANDIDATES)

with open("/Users/thomaswileman/advent_of_code/advent_of_code_2020/day_21/input.txt") as f:
    raw = f.read()
    foods = [Food.parse(line) for line in raw.split("\n")]
    print(count_no_allergens(foods))
    cands = candidates(foods)
    print(arrange(cands))