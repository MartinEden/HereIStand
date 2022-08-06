from models import connection_types, space_types, powers


def exit_if_any_problems(func):
    def inner(*arg):
        problems = list(func(*arg))
        if problems:
            for problem in problems:
                print(problem)
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
def validate_connections_basic(connections, spaces):
    for duplicate in duplicates_in(str(c) for c in connections):
        yield f'Duplicate connection: {duplicate}'

    for connection in connections:
        if connection.from_ not in spaces:
            yield f"Connection to '{connection.to}' from unknown space '{connection.from_}'"
        if connection.to not in spaces:
            yield f"Connection from '{connection.from_}' to unknown space '{connection.to}'"   

        if connection.type not in connection_types:
            yield f"Connection '{connection}' has unknown type '{connection.type}'"


@exit_if_any_problems
def validate_connections(spaces):
    for space in spaces.values():
        for connection in space.connections:
            if connection.from_ != space.name:
                yield f"Space '{space.name}' has connection '{connection}' that should belong to '{connection.from_}'"

            to_space = spaces[connection.to]
            reciprocal = to_space.get_connection_to(space.name)
            if reciprocal is None:
                yield f"Connection '{connection}' does not have reciprocal"

            if connection.type != reciprocal.type:
                yield f"Connection '{connection}' is of type '{connection.type}', but the reciprocal connection '{reciprocal}' has type '{reciprocal.type}'"
            if space.type != "sea" and to_space.type == "sea" and connection.type != "port":
                yield f"Connection '{connection}': Expected type 'port', was actually '{connection.type}'"
            if space.type == "sea" and to_space.type == "sea" and connection.type != "sea":
                yield f"Connection '{connection}': Expected type 'sea', was actually '{connection.type}'"                
