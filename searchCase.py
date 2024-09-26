import sys,os
import indexList as iL
def getContestType():#コンテストの種類を返す
    return False,["abc","arc","agc"]

def getContestNumber(contestType:str,indexListData:dict):#ストックされているコンテストの番号を返す、無ければ空配列
    result=[]
    for i in list(indexListData.keys()):
        if i[:3]==contestType.lower():
            result.append(i[3:])
    return False,result

def getContestSet(contestStr:str,indexListData:dict): #コンテストのセット(A~Hのいずれか)を返す、無ければFalse
    if contestStr not in indexListData:
        return False,"指定のコンテストのテストケースが見つかりません。"
    else:
        return False,list(indexListData[contestStr].keys())[1:]#_filesを無視する

def getContestCase(contestStr:str,QuestionSet:str,indexListData:dict):#コンテストのセットに含まれるテストケースを返す、無ければFalse
    if QuestionSet not in indexListData[contestStr]:
        return False,"該当セットがありません。"
    else:
        return False,indexListData[contestStr][QuestionSet]["in"]["_files"]

def searchTestCase(contestStr:str,QuestionSet:str,testCase:str,indexListData:dict):#テストケースの名前が何番目かを返す(0-indexed)、無ければFalse
    if testCase not in indexListData[contestStr][QuestionSet]["in"]["_files"]:
        return False,"指定のテストケースが見つかりません。"
    else:
        return True,indexListData[contestStr][QuestionSet]["in"]["_files"].index(testCase)

def getTestCasePath(contestStr:str,QuestionSet:str,testCaseNumber:int,indexListData:dict,inOrOut:str): #テストケースの番号(0-indexed)からパスを返す、無ければFalse
    if len(indexListData[contestStr][QuestionSet]["in"]["_files"])<testCaseNumber or testCaseNumber<0:
        return False,"指定のテストケースが見つかりません。"
    else:
        return True,os.path.join(contestStr,QuestionSet,inOrOut,indexListData[contestStr][QuestionSet][inOrOut]["_files"][testCaseNumber])

def main(args=[],inOrOut="in",directory="out"):
    #引数0個目にコンテストの種類、1個目にコンテストの番号、2個目にセット、3個目にテストケースの番号、4個目にinかoutを入れる
    indexListData=iL.getList("indexList.json")
    args=args
    if len(args)==0:#引数がない場合はコンテストの種類を返す
        return getContestType()
    if len(args)==1:#引数が1つの場合はコンテストの番号を返す、なければ[]
        return getContestNumber(args[0],indexListData)
    elif len(args)==2:#引数が2つの場合はコンテストのセットを返す、なければFalse
        contestStr=args[0]+args[1]
        return getContestSet(contestStr,indexListData)
    elif len(args)==3:#引数が3つの場合はコンテストのセットに含まれるテストケースを返す、なければFalse
        args[0]=args[0].lower()
        args[2]=args[2].upper()
        contestStr=args[0]+args[1]
        return getContestCase(contestStr,args[2],indexListData)
    elif len(args)==4:#引数が4つの場合はテストケースのパスを返す、なければFalse
        args[0]=args[0].lower()
        args[2]=args[2].upper()
        contestStr=args[0]+args[1]
        #例外をはじく
        if args[0] not in ["abc","arc","agc"]:
            return False,"形式が間違っています。ABC,ARC,AGCのいずれかを入力してください。 > "+args[0]
        elif args[2] not in ["A","B","C","D","E","F","G","H"]:
            return False,"形式が間違っています。A~HかXを入力してください > "+args[2]
        elif args[0]+args[1] not in indexListData.keys():
            return False,"指定のコンテストのテストケースが見つかりません。日をおいてから再度お試しください。 > "+args[0]+args[1]
        
        if args[3].endswith(".txt"):#引数が数字でない場合はテストケース名を返す
            testCaseNumber=searchTestCase(contestStr,args[2],args[3],indexListData)#テストケースの番号を取得
            if testCaseNumber[0]==False:#テストケースの番号が見つからなかった場合はFalseを返す
                return False,"指定の名前のテストケースが見つかりませんでした。"
            else:#テストケースの番号が見つかった場合はパスを返す
                filename_in=getTestCasePath(contestStr,args[2],testCaseNumber[1],indexListData,"in")
                filename_out=getTestCasePath(contestStr,args[2],testCaseNumber[1],indexListData,"out")
                if filename_in[0] and filename_out[0]:
                    return True,os.path.join(directory,filename_in[1]),os.path.join(directory,filename_out[1])
                else:
                    return False,"指定の名前のテストケースが見つかりませんでした。"
        else:#引数が数字の場合はその名前のテストケースを返す
            filename_in=getTestCasePath(contestStr,args[2],int(args[3])-1,indexListData,"in")
            filename_out=getTestCasePath(contestStr,args[2],int(args[3])-1,indexListData,"out")
            if filename_in[0] and filename_out[0]:
                return True,os.path.join(directory,filename_in[1]),os.path.join(directory,filename_out[1])
            else:
                return False,"指定の番号のテストケースが見つかりませんでした。"
    else:#引数が6つ以上の場合はFalse
        return False,"引数が多すぎます。"

if __name__=="__main__":
    args=[]
    args.append(input("コンテストの種類を入力してください:"))
    args.append(input("番号"))
    args.append(input("セット"))
    args.append(input("ケース"))
    print(main(args))




