from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
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

class Handler(FileSystemEventHandler):
    def __init__(self):
        self.json_obj = JSONHandler("plugins.json")

    def on_created(self, event):
        plugin_name = event.src_path.split("\\")[-1]
        if self._check_file_name(plugin_name):
            self.json_obj.add_json(plugin_name)
            print(f"added {plugin_name} to json")

    def on_deleted(self, event):
        plugin_name = event.src_path.split("\\")[-1]
        if self._check_file_name(plugin_name):
            self.json_obj.remove_json(plugin_name)
            print(f"removed {plugin_name} from json")
        
    def _check_file_name(self, plugin_name):
        return plugin_name.endswith(".py") and not plugin_name.startswith(("config.", ".", "default."))

def watch(path):
    observer = Observer()
    observer.schedule(Handler(), path, recursive=True)

    observer.start()
    print(f"Watching path: {path}")

    try:
        while True:
            time.sleep(1)
    except:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    watch(".\\plugins")