##
# File: dataFunctions.py
# Brief: Password Manager calass constructor and functions
# Autor: Michal Ľaš

from pathlib import Path
import json as js

class dataFunctions:

    def __init__(self):
        self.name = None
        self.email = None
        self.pw = None
        self.description = None


    ##
    # Function return data loaded from .json file
    def load_data(self):
        path = Path(__file__).parent / "../data/data.json"
        with path.open("r") as f:
            data = js.load(f)

        return data

    ##
    # Add new record to database
    def create_record(self, data, category, new_record):
        path = Path(__file__).parent / "../data/data.json"
        with path.open("w") as f:
            data[category].append(new_record)
            js.dump(data, f)

    ##
    # Edit existing record in database
    def edit_record(self, data, category, index, item, new_data):
        path = Path(__file__).parent / "../data/data.json"
        with path.open("w") as f:
            data[category][index][item] = new_data
            js.dump(data, f)


    ##
    # Delete existing record
    def delete_record(self, data, category, name):
        item = data[category][dataFunctions.find_record(self, data[category], name)]

        path = Path(__file__).parent / "../data/data.json"
        with path.open("w") as f:
            data[category].remove(item)
            js.dump(data, f)


    ##
    # Function return index of searching item or -1 if item was not found
    def find_record(self, data, searching_item):
        for i in range(len(data)):
            if (data[i]["name"] == searching_item):
                return i
        return -1    
        