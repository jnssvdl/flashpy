# other module
import json

class InformationManager():
    def __init__(self, file_name, data):
        # INITIALIZING THE INFORMATION MANAGER CLASS.
        self.file_name = file_name
        self.data = data

    """LOAD FLASHCARD SETS FROM A FILE AND UPDATE THE DATA DICTIONARY"""
    def loads_set_from_file(self):
        with open(self.file_name, "a+") as file:
            file.seek(0)
            try:
                set_data = json.load(file)
            except:
                pass
            else:
                self.data.update(set_data)

    """UPDATE THE FLASHCARD SETS IN THE FILE WITH THE DATA DICTIONARY"""
    def update_sets_to_file(self):
        with open(self.file_name, "w") as file:
            json.dump(self.data, file, indent=4)
