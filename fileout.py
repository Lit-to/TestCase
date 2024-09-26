import datetime

def printf(*args):
    print(datetime.datetime.now(),*args)
    with open('../log.txt', 'w',encoding="utf-8") as f:
        print(datetime.datetime.now(),*args,file=f)


