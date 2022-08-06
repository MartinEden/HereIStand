import sys

from models import connection_types, space_types, powers


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
def validate_spaces(spaces):
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
