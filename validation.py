import sys
from typing import List

from models import connection_types, space_types, powers, Space


def exit_if_any_problems(func):
    def inner(*arg):
        problems = list(func(*arg))
        if problems:
            for problem in problems:
                print(problem)
            print(f"Exiting with {len(problems)} problems")
            sys.exit(1)

    return inner


def duplicates_in(some_list):
    seen = set()
    for x in some_list:
        if x in seen:
            yield x
        else:
            seen.add(x)


@exit_if_any_problems
def validate_spaces(spaces: List[Space]):
    for duplicate in duplicates_in(sp.name for sp in spaces):
        yield f'Duplicate space: {duplicate}'

    for space in spaces:
        if space.type not in space_types:
            yield f"Space '{space.name}' has invalid type '{space.type}'"
        if space.home_power not in powers:
            yield f"Space '{space.name}' has invalid home power '{space.home_power}'"

        if space.type == "sea" and space.home_power != "sea":
            yield f"Space '{space.name}' is a sea zone, but home_power is not 'sea'"
        if space.type != "sea" and space.home_power == "sea":
            yield f"Space '{space.name}' is not a sea zone, but home_power is 'sea'"


class SpaceCountCheck(object):
    def __init__(self, descriptor, expected_number, predicate):
        self.descriptor = descriptor
        self.expected_number = expected_number
        self.predicate = predicate

    def perform(self, spaces):
        actual = len([x for x in spaces if self.predicate(x)])
        if self.expected_number != actual:
            return f"Expected {self.expected_number} {self.descriptor} but there were {actual}"
        else:
            return None


@exit_if_any_problems
def validate_expected_space_counts(spaces: List[Space]):
    checks = [
        # By type of space
        SpaceCountCheck("capitals", 6, lambda x: x.type == "capital"),
        SpaceCountCheck("fortresses", 9, lambda x: x.type == "fortress"),
        SpaceCountCheck("electorates", 6, lambda x: x.type == "electorate"),

        # Right number of keys per major power. Note that `is_key()` includes spaces of type 'capital'
        SpaceCountCheck("Ottoman keys", 5, lambda x: x.is_key() and x.home_power == "ottoman"),
        SpaceCountCheck("Hapsburg keys", 7, lambda x: x.is_key() and x.home_power == "hapsburg"),
        SpaceCountCheck("English keys", 4, lambda x: x.is_key() and x.home_power == "england"),
        SpaceCountCheck("French keys", 5, lambda x: x.is_key() and x.home_power == "france"),
        SpaceCountCheck("Papal keys", 2, lambda x: x.is_key() and x.home_power == "papacy"),
        SpaceCountCheck("Protestant keys", 0, lambda x: x.is_key() and x.home_power == "protestant"),

        # Right number of keys for independents and minor powers.
        SpaceCountCheck("Independent keys", 4, lambda x: x.is_key() and x.home_power == "independent"),
        SpaceCountCheck("Scottish keys", 1, lambda x: x.is_key() and x.home_power == "scotland"),
        SpaceCountCheck("Genoese keys", 1, lambda x: x.is_key() and x.home_power == "genoa"),
        SpaceCountCheck("Hungarian keys", 3, lambda x: x.is_key() and x.home_power == "hungary"),
        SpaceCountCheck("Venetian keys", 1, lambda x: x.is_key() and x.home_power == "venice"),
    ]
    for check in checks:
        result = check.perform(spaces)
        if result:
            yield result


@exit_if_any_problems
def validate_connection_rows(connections, space_lookup):
    for duplicate in duplicates_in(str(c) for c in connections):
        yield f'Duplicate connection: {duplicate}'

    for connection in connections:
        if connection.origin not in space_lookup:
            yield f"Connection to '{connection.dest}' from unknown space '{connection.origin}'"
        if connection.dest not in space_lookup:
            yield f"Connection from '{connection.origin}' to unknown space '{connection.dest}'"

        if connection.type not in connection_types:
            yield f"Connection '{connection}' has unknown type '{connection.type}'"


@exit_if_any_problems
def validate_connections(space_lookup):
    for space in space_lookup.values():
        for connection in space.connections:
            target_space = space_lookup[connection.dest]
            reciprocal = target_space.get_connection_to(space.name)
            if reciprocal is None:
                yield f"Connection '{connection}' does not have reciprocal"
            else:
                if connection.type != reciprocal.type:
                    yield f"Connection '{connection}' is of type '{connection.type}', but the reciprocal connection '{reciprocal}' has type '{reciprocal.type}'"
                if space.type != "sea" and target_space.type == "sea" and connection.type != "port":
                    yield f"Connection '{connection}': Expected type 'port', was actually '{connection.type}'"
                if space.type == "sea" and target_space.type == "sea" and connection.type != "sea":
                    yield f"Connection '{connection}': Expected type 'sea', was actually '{connection.type}'"
