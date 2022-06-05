import json

class JSONHandler:
    def __init__(self, json_name):
        self.json_name = json_name

    def add_json(self, plugin_name):
        with open(self.json_name, "r+") as file:
            data = json.load(file)

            data["plugins"].append(plugin_name)
            file.seek(0)
            
            json.dump(data, file, indent=4)

    def remove_json(self, plugin_name):
        with open(self.json_name, "r+") as file:
            data = json.load(file)

            file.truncate(0)
            data["plugins"] = [plug for plug in data["plugins"] if plug != plugin_name]
            file.seek(0)

            json.dump(data, file, indent=4)

    def _print_json(self):
        with open(self.json_name, "r") as file:
            data = json.load(file)
            print(data)