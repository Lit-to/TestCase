import json
import os
import indexList as iL


def getList(path:str):
    with open(path,mode="r") as f:
        data=json.load(f)#jsonデータをdictとして取得
    return data

def dump(path:str,data:dict):
    with open(path,mode="w") as f:
        json.dump(data,f)#dictデータをjsonに出力

def checkList(type:str,file:str,data:dict):
    for i in data[type]:
        if file == i:
            return True
    return False

def getFileStructure(path:str,directory=""):
    structure=dict()
    if directory=="":
        directory=path
    #ファイル構造を取得する関数
    #ただし制約として、フォルダ名が_filesのものはないものとする
    folder=os.listdir(path)
    structure["_files"]=[]
    for i in folder:
        if os.path.isdir(os.path.join(path,i)):
            structure[i]=getFileStructure(os.path.join(path,i),i)
        else:
            structure["_files"].append(i)
    return structure

if __name__=="__main__":
    structure=getFileStructure("out")
    dump("indexList.json",structure)




