import sys,os
import indexList as iL

# def getContestStr(contestType:str,contestNumber:str): #回に応じて大文字か小文字かを判定して適切な文字列を返す
#     if contestType.lower()=="abc":
#         if int(contestNumber)<=197:
#             return contestType.upper()+contestNumber
#         elif 197<int(contestNumber):
#             return contestType.lower()+contestNumber
#     elif contestType.lower()=="arc":
#         if int(contestNumber)<=197:
#             return contestType.upper()+contestNumber
#         elif 197<int(contestNumber):
#             return contestType.lower()+contestNumber
#     elif contestType.lower()=="agc":
#         if int(contestNumber)<=197:
#             return contestType.upper()+contestNumber
#         elif 197<int(contestNumber):
#             return contestType.lower()+contestNumber

def getContestType():#コンテストの種類を返す
    return ["abc","arc","agc"]

def getContestNumber(contestType:str,indexListData:dict):#ストックされているコンテストの番号を返す、無ければ空配列
    result=[]
    for i in list(indexListData.keys()):
        if i[:3]==contestType.lower():
            result.append(i[3:])
    return result
    # if contestType not in indexListData:
    #     return False
    # else:
    #     return indexListData[contestType]


def getContestSet(contestStr:str,indexListData:dict): #コンテストのセット(A~Hのいずれか)を返す、無ければFalse
    if contestStr not in indexListData:
        return False
    else:
        return list(indexListData[contestStr].keys())[1:]#_filesを無視する

def getContestCase(contestStr:str,QuestionSet:str,indexListData:dict):#コンテストのセットに含まれるテストケースを返す、無ければFalse
    if QuestionSet not in indexListData[contestStr]:
        return False
    else:
        return indexListData[contestStr][QuestionSet]["in"]["_files"]

def searchTestCase(contestStr:str,QuestionSet:str,testCase:str,indexListData:dict):#テストケースの名前が何番目かを返す(0-indexed)、無ければFalse
    if testCase not in indexListData[contestStr][QuestionSet]["in"]["_files"]:
        return False
    else:
        return indexListData[contestStr][QuestionSet]["in"]["_files"].index(testCase)

def getTestCasePath(contestStr:str,QuestionSet:str,testCaseNumber:str,indexListData:dict,inOrOut:str): #テストケースの番号(0-indexed)からパスを返す、無ければFalse
    if len(indexListData[contestStr][QuestionSet]["in"]["_files"])<testCaseNumber or testCaseNumber<0:
        return False
    else:
        return os.path.join(contestStr,QuestionSet,inOrOut,indexListData[contestStr][QuestionSet][inOrOut]["_files"][testCaseNumber])

def main(args:list,inOrOut="in",directory="out"):
    #引数は0は無視し、1個目にコンテストの種類、2個目にコンテストの番号、3個目にセット、4個目にテストケースの番号、5個目にinかoutを入れる
    indexListData=iL.getList("indexList.json")
    args=args[1:]
    if len(args)==0:#引数がない場合はコンテストの種類を返す
        return getContestType()
    elif len(args)==1:#引数が1つの場合はコンテストの番号を返す、なければ[]
        return getContestNumber(args[0],indexListData)
    elif len(args)==2:#引数が2つの場合はコンテストのセットを返す、なければFalse
        contestStr=args[0]+args[1]
        return getContestSet(contestStr,indexListData)
    elif len(args)==3:#引数が3つの場合はコンテストのセットに含まれるテストケースを返す、なければFalse
        contestStr=args[0]+args[1]
        return getContestCase(contestStr,args[2],indexListData)
    elif len(args)==4:#引数が4つの場合はテストケースのパスを返す、なければFalse
        contestStr=args[0]+args[1]
        if args[3].isdigit()==False:#引数が数字では場合はテストケース名を返す
            testCaseNumber=searchTestCase(contestStr,args[2],args[3],indexListData)#テストケースの番号を取得
            if testCaseNumber==False:
                return False
            else:#テストケースの番号が見つかった場合はパスを返す
                return getTestCasePath(contestStr,args[2],testCaseNumber,indexListData,inOrOut)
        else:#引数が数字でない場合はその名前のテストケースを返す
            filename=getTestCasePath(contestStr,args[2],int(args[3])-1,indexListData,inOrOut)
            if filename!=False:
                return os.path.join(directory,filename)
            else:
                return False
    else:#引数が6つ以上の場合はFalse
        return False

if __name__=="__main__":
    print(main(args=sys.argv))




