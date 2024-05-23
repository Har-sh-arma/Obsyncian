import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import obsync

class Watcher:
    # Set the directory on watch
    watchDirectory = obsync.cwd
 
    def __init__(self):
        self.observer = Observer()
 
    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.watchDirectory, recursive = True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Observer Stopped")
 
        self.observer.join()
 
 
class Handler(FileSystemEventHandler):
 
    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None
 
        elif event.event_type == 'created':
            # Event is created, you can process it now
            name = (".\\"+"\\".join(event.src_path.split("\\")[-2:]))
            try:
                print("Creating File: " + name)
                obsync.id_map[name.split("\\")[-2]]
            except KeyError:
                print("Creating Folder: " + name.split("\\")[-2])
                file = obsync.drive.CreateFile({'title': name.split("\\")[-2], "parents":[ {'id':'1JX6I6LOYQgjfDSlSZXyLKKeBMrJE-su0'}], 'mimeType': 'application/vnd.google-apps.folder'})
                file.Upload()
                # time.sleep(5)
                obsync.id_map[name.split("\\")[-2]] = file['id']
                print(obsync.id_map[name.split("\\")[-2]])
                obsync.sync_id_map()
            finally:
                file = obsync.drive.CreateFile({'title': name.split("\\")[-1], "parents":[ {'id':obsync.id_map[name.split("\\")[-2]]}]})
                file.SetContentFile(event.src_path)
                file.Upload()
                obsync.id_map[name] = file['id']
        elif event.event_type == 'modified':
            print("File Modified: % s" %  (".\\"+"\\".join(event.src_path.split("\\")[-2:])))
            # Event is modified, you can process it now
            try:
                file = obsync.drive.CreateFile({'id':obsync.id_map[(".\\"+"\\".join(event.src_path.split("\\")[-2:]))]})
                file.SetContentFile(event.src_path)
                file.Upload()
                print("File Updated: % s" %  (".\\"+"\\".join(event.src_path.split("\\")[-2:])))
            except KeyError:
                print("File Not Updated: % s" %  (".\\"+"\\".join(event.src_path.split("\\")[-2:])))
             
 
if __name__ == '__main__':
    watch = Watcher()
    watch.run()