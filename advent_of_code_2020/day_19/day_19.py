from __future__ import annotations
from typing import NamedTuple, List, Optional, Tuple, Iterator
from collections import deque

# Tough because assumed rules were in order and they weren't
class Rule(NamedTuple):
    id : int
    literal: Optional[str] = None
    subrules: ListList[[int]] = []
    
    @staticmethod
    def parse(line:str) -> Rule:
        rule_id, rest = line.strip().split(": ")
        if rest.startswith('"'):
            return Rule(id = int(rule_id), literal = rest[1:-1])
        
        if "|" in rest:
            parts = rest.split(" | ")
        else:
            parts = [rest]
        
        return Rule(id = int(rule_id), 
                    subrules = [[int(n) for n in part.split()] for part in parts])

def check(s: str, rules: List[Rule]) -> bool:
    """
    Returns True if s is a match for rules[0]
    """
    # queue of pairs (remaining string, remaining rules)
    q = deque([(s, [0])])
    
    while q:
        # separate the sequence of letters (s) from the rule ids ([0])
        s, rule_ids = q.popleft()
        # used all string and all rules so a match
        if not s and not rule_ids:
            return True
        
        # use string or rules but not both, dead end, continue
        elif not s or not rule_ids:
            continue
        
        # have both s and rule_ids. try the first rule.
        elif len(rule_ids) > len(s):
            continue
        rule = rules[rule_ids[0]]
        rule_ids = rule_ids[1:]
        
        # first rule is literal so if it matches the first character add remaining string and rules to queue.
        if rule.literal and s[0] == rule.literal:
            q.append((s[1:], rule_ids))
            
        # otherwise, have sequences of subrules.
        # prepend each remaining sequence to remaining rule_ids and add to new list with s
        
        else:
            for subrule_ids in rule.subrules:
                q.append((s, subrule_ids + rule_ids))
                
    # queue is exhaused and never found match            
    return False

def parse(raw: str):
    raw_rules, raw_strings = raw.split("\n\n")
    rules = [Rule.parse(rr) for rr in raw_rules.split("\n")]
    rules.sort()
    assert all(rule.id == i for i, rule in enumerate(rules))
    strings = raw_strings.split("\n")
    return rules, strings

RAW = """0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb"""


RULES, STRINGS = parse(RAW)

for s in STRINGS:
    print(s, check(s, RULES))

assert sum(check(s, RULES) for s in STRINGS) == 2

with open("/Users/thomaswileman/advent_of_code/advent_of_code_2020/day_19/input.txt") as f:
    raw = f.read()
    rules, strings = parse(raw)
    
    print(sum(check(s, rules) for s in strings))

rules[8] = Rule.parse("8: 42 | 42 8")
rules[11] = Rule.parse("11: 42 31 | 42 11 31")

good = 0
for i, s in enumerate(strings):
    if check(s, rules):
        good += 1
print(good)