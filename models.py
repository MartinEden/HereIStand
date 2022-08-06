space_types = ['normal', 'fortress', 'key', 'capital', 'electorate', 'sea']
powers = [
    'england',
    'protestant',
    'scotland',
    'france',
    'papacy',
    'hapsburg',
    'hapsburg/ottoman',
    'ottoman',
    'hungary',
    'genoa',
    'venice',
    'independent',
    'sea'
]
connection_types = ['normal', 'pass', 'port', 'sea']


class Space(object):
    def __init__(self, name, type_, home_power):
        self.name = name
        self.type = type_
        self.home_power = home_power
        self.connections = []

    @classmethod
    def from_csv_row(cls, row):
        return Space(name=row[0], type_=row[1], home_power=row[2])

    def get_connection_to(self, space_name):
        for connection in self.connections:
            if connection.dest == space_name:
                return connection
        return None

    def is_key(self):
        return self.type == "key" or self.type == "capital"

    def __str__(self):
        return f"Space:{self.name}"


class ConnectionRow(object):
    """Represents a row from connections.csv"""

    def __init__(self, row):
        self.origin = row[0]
        self.dest = row[1]
        self.type = row[2]

    def __str__(self):
        return f"{self.origin} -> {self.dest}"


class Connection(object):
    """Represents a connection attached to a Space object - thus it doesn't need an 
       origin, as that's implicit"""

    def __init__(self, dest, type_):
        self.dest = dest
        self.type = type_
