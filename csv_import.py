import csv
from models import Space, Connection
import validation

def import_spaces(path):
    with open(path) as file:
        reader = csv.reader(file, delimiter=',')
        next(reader) # skip header row
        for row in reader:
            yield Space.from_csv_row(row)


def import_connections(path):
    with open(path) as file:
        reader = csv.reader(file, delimiter=',')
        next(reader) # skip header row
        for row in reader:
            yield Connection(row)


def import_csv(spaces_path, connections_path):    
    spaces = list(import_spaces(spaces_path))
    connections = list(import_connections(connections_path))
    return spaces, connections


def import_and_validate():
    spaces, connections = import_csv("spaces.csv", "connections.csv")

    validation.validate_spaces(spaces)
    space_lookup = { s.name: s for s in spaces }

    validation.validate_connections_basic(connections, space_lookup)

    for connection in connections:
        from_space = space_lookup[connection.origin]
        from_space.connections.append(connection)
    
    validation.validate_connections(space_lookup)
    return spaces
