from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive



gauth = GoogleAuth()
drive = GoogleDrive(gauth)

def createFolder(folderName, parentId='root'):
    folder = drive.CreateFile({'title': folderName, "parents":[ {'id':parentId}], 'mimeType': 'application/vnd.google-apps.folder'})
    folder.Upload()
    return folder['id']

def createFile(fileName, parentId, fileContentPath):
    file = drive.CreateFile({'title': fileName, "parents":[ {'id':parentId}]})
    file.SetContentFile(fileContentPath)
    file.Upload()
    return file['id']

def modifyFile(fileId, fileContentPath):
    file = drive.CreateFile({'id':fileId})
    file.SetContentFile(fileContentPath)
    file.Upload()

def deleteFileorFolder(objectId):
    file = drive.CreateFile({'id':objectId})
    file.Delete()

def trashFileorFolder(objectId):
    file = drive.CreateFile({'id':objectId})
    file.Trash()

def moveFileorFolder(objectId, parentId, objectName):
    print(f"{objectId} {parentId} {objectName}")
    file = drive.CreateFile({'id':objectId})
    file['title'] = objectName
    file['parents'] = [{'id':parentId}]
    file.Upload()



if __name__ == "__main__":
    print("drivePack.py is being run directly")

