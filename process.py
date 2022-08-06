#!/usr/bin/env python3
import csv_import
import json
import os.path

class ObjectEncoder(json.JSONEncoder):
        def default(self, o):
            return o.__dict__


if __name__ == '__main__':   
    json_path = 'spaces.json'    
    spaces = csv_import.import_and_validate()
    print(f"Imported {len(spaces)} spaces without any errors.")

    with open(json_path, 'w') as f:
        json.dump(spaces, f, cls = ObjectEncoder, indent=4)
    print(f"Exported successfully to '{os.path.abspath(json_path)}'")
