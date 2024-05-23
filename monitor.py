import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
# import drivePack as dp
from syncPack import PATH, idm, ignorable_folders,dp

class Watcher:
    # Set the directory on watch
    watchDirectory = PATH
 
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
        for i in ignorable_folders:             #ignore ignorable folders
            if i in event.src_path:
                # print("ignored")
                return
        
        print(f"{type(event)} detected in: {event.src_path}")
        if event.event_type == 'created':
            if event.is_directory:
                name = event.src_path
                print("Creating Folder : "+name.split(PATH)[-1])
                parent_id =  "\\".join(name.split(PATH)[-1].split('\\')[0:-1])
                idm[name.split(PATH)[-1]] =  dp.createFolder(name.split('\\')[-1], idm[parent_id])
            else:
                name = event.src_path
                print("Creating File : "+name.split(PATH)[-1])
                parent_id =  "\\".join(name.split(PATH)[-1].split('\\')[0:-1])
                idm[name.split(PATH)[-1]] = dp.createFile(name.split('\\')[-1], idm[parent_id], name)
        if event.event_type == 'deleted':
            name = event.src_path
            print("Deleting : "+name.split(PATH)[-1])
            dp.deleteFileorFolder(idm[name.split(PATH)[-1]])
            idm.pop(name.split(PATH)[-1])
        if event.event_type == 'modified':
            if event.is_directory:
                return
            name = event.src_path
            print("Modifying : "+name.split(PATH)[-1])
            dp.modifyFile(idm[name.split(PATH)[-1]], name)
        if event.event_type == 'moved':
            name = event.src_path
            dest = event.dest_path
            newName = dest.split("\\")[-1]
            print("Moving : "+name + " to "+ dest)
            dp.moveFileorFolder(idm[name.split(PATH)[-1]], idm[dest.split(PATH)[-2]], newName)
            idm[dest.split(PATH)[-1]] = idm.pop(name.split(PATH)[-1])
            


if __name__ == '__main__':
    
    w = Watcher()
    w.run()
