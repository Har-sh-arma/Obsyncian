import pandas as pd
import os

class idMap:
    def __init__(self):
        self.idMap = {}
        self.getMap()
    
    def getMap(self):
        if os.path.exists('id_map.csv'):
            df = pd.read_csv('id_map.csv', header=None).to_dict(orient='index')
            for i in df:
                self.idMap[df[i][0]] = df[i][1]
    def setMap(self):
        df = pd.DataFrame.from_dict(self.idMap, orient='index')
        df.to_csv('id_map.csv', header=False)

    def __setitem__(self, __name: str, __value : any) -> None:
        self.idMap[__name] = __value
        self.setMap()

    def __getitem__(self, __name: str) -> any:
        self.getMap()
        if __name == "":
            return self.idMap["__ROOT__"]
        return self.idMap[__name]
    
    def pop(self, __name: str) -> any:
        res = self.idMap.pop(__name , None)
        self.setMap()
        return res
    
if __name__ == '__main__':
    print("Kaay kartoy bala, Ha package aahe")