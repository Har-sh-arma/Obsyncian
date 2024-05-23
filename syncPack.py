import os
import glob
import drivePack as dp
from mapPack import idMap

'''
Set path to your Obsidian base folder as environment variable "Obsidian_Base"
'''

idm = idMap()

PATH = os.environ["Obsidian_Base"]

ignorable_folders = ["\\__pycache__", "\\dev", "\\.obsidian"]


def CrawlandCreate(path):
    for name in glob.glob(path+"/*"):
        if(name.split(PATH)[-1] in ignorable_folders):
            continue
        print(name.split(PATH)[-1])
        if(os.path.isdir(name)):
            print("Creating Folder : "+name.split(PATH)[-1])
            parent_id =  "\\".join(name.split(PATH)[-1].split('\\')[0:-1])
            idm[name.split(PATH)[-1]] =  dp.createFolder(name.split('\\')[-1], idm[parent_id])
        else:
            print("Creating File : "+name.split(PATH)[-1])
            # print(f"Parent id: "+  "\\".join(name.split(PATH)[-1].split('\\')[0:-1]))
            parent_id =  "\\".join(name.split(PATH)[-1].split('\\')[0:-1])
            idm[name.split(PATH)[-1]] = dp.createFile(name.split('\\')[-1], idm[parent_id], name)
        CrawlandCreate(name)


if __name__== '__main__':
    # in actuality this ID will be create using the createFolder function
    dp.deleteFileorFolder(idm[""])
    idm['__ROOT__']= dp.createFolder("Based")
    print(idm[""])
    CrawlandCreate(PATH)
