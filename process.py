#!/usr/bin/env python3
import csv
import sys
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



if __name__ == '__main__':        
    space_list, connections = import_csv("spaces.csv", "connections.csv")

    validation.validate_spaces(space_list)
    spaces = { s.name: s for s in space_list }

    validation.validate_connections_basic(connections, spaces)

    for connection in connections:
        from_space = spaces[connection.from_]
        print(from_space.connections)
        from_space.connections.append(connection)
        print(from_space.connections)
        sys.exit(0)

    validation.validate_connections(spaces)
