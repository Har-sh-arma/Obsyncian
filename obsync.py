from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import pandas as pd
import os
import glob

gauth = GoogleAuth()
drive = GoogleDrive(gauth)
id_map = {}
'''
file1 = drive.CreateFile({'title': 'Hello.txt'})
file1.Upload() # Upload the file.
print('title: %s, id: %s' % (file1['title'], file1['id']))

# creating the obsync folder

file_metadata = {
    'title': "based",
    'mimeType': 'application/vnd.google-apps.folder'
}

file = drive.CreateFile(file_metadata)
file.Upload()

print('title: %s, id: %s' % (file['title'], file['id']))

# folder details
# title: based, id: 1JX6I6LOYQgjfDSlSZXyLKKeBMrJE-su0
 '''
def initiate():
    for name in glob.glob("*.*"):
        if name not in ig_files:
            if name not in id_map:
                print("Creating File: " + name)
                file = drive.CreateFile({'title': name, "parents":[ {'id':'1JX6I6LOYQgjfDSlSZXyLKKeBMrJE-su0'}]})
                file.Upload()
                id_map[name] = file['id']

    for name in glob.glob("./*/"):
        if name.split("\\")[1] not in id_map:
            print("Creating Folder: " + name.split("\\")[1])
            folder = drive.CreateFile({'title': name.split("\\")[1], "parents":[ {'id':'1JX6I6LOYQgjfDSlSZXyLKKeBMrJE-su0'}], 'mimeType': 'application/vnd.google-apps.folder'})
            folder.Upload()
            id_map[name.split("\\")[1]] = folder['id']

        else:
            for n in glob.glob(".\\"+name.split("\\")[1]+"\\*.*"):
                print(n.split("\\")[-1])
                if n not in id_map:
                    print("Creating File: " + n.split("\\")[-1])
                    file = drive.CreateFile({'title': n.split("\\")[-1], "parents":[ {'id':id_map[name.split("\\")[1]]}]})
                    file.SetContentFile(n)
                    file.Upload()
                    id_map[n] = file['id']
                else:
                    print("File already exists: " + n.split("\\")[-1])


#replicate the entire folder structure


def sync_id_map():
    df = pd.DataFrame.from_dict(id_map, orient='index')
    df.to_csv('id_map.csv', header=False)      

# initiate()

'''
for name in glob.glob("*.*"):
    if name not in ig_files:
        print("Creating File: " + name)
        file = drive.CreateFile({'title': name, "parents":[ {'id':'1JX6I6LOYQgjfDSlSZXyLKKeBMrJE-su0'}]})
        file.Upload()
        id_map[name] = file['id']
'''




cwd = os.getcwd()
ig_files = ["obsync.py", "client_secrets.json", "credentials.json", "settings.yaml"]
ig_folders = [".venv", "__pycache__"]
id_map = {}
if(os.path.exists('id_map.csv')):
    id_map_improper = pd.read_csv('id_map.csv', header=None).to_dict(orient='index')
    for i in id_map_improper:
        id_map[id_map_improper[i][0]] = id_map_improper[i][1]

# print(id_map)

if __name__ == '__main__':
    # Getting stored drive Ids
    initiate()  

sync_id_map()
