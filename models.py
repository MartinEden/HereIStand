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
    def __init__(self, name, type_, home_power, connections=[]):
        self.name = name
        self.type = type_
        self.home_power = home_power
        self.connections = [connections]

    @classmethod
    def from_csv_row(cls, row):
        return Space(name = row[0], type_ = row[1], home_power = row[2])

    def get_connection_to(self, space_name):
        for connection in self.connections:
            if connection.to == space.name:
                return connection
        return None


class Connection(object):
    def __init__(self, row):
        self.from_ = row[0]
        self.to = row[1]
        self.type = row[2]

    def __str__(self):
        return f"{self.from_} -> {self.to}"
