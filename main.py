from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from core import JSONHandler
import time

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