class com_class():
    def __init__(self,tmpStr):
        li=tmpStr.split("\t")
        self.chr=li[0]
        self.st=li[1]
        self.ed=li[2]
    def ismatch(self,other):
        if self.chr==other.chr and self.st==other.st and self.ed==other.ed:
            return True
        else:
            return False
sourceFile=open("wgs.ALL")
refFile=open("wgs.INS")
relFile=open("wgs.NotINS","w")
refList=[]
while 1:
    tmpStr=refFile.readline()
    if tmpStr=='':
        break
    refList.append(com_class(tmpStr))
while 1:
    tmpStr=sourceFile.readline()
    if tmpStr=='':
        break
    tmpCla=com_class(tmpStr)
    flag=False
    for i in range(len(refList)):
        if refList[i].ismatch(tmpCla):
            flag=True
            break
    if flag==False:
        print(tmpStr,file=relFile,end='')
'''
sourceFile=open("wgs.notDEL")
while 1:
    tmpStr=sourceFile.readline()
    if tmpStr=='':
        break
    tmpCla=com_class(tmpStr)
    flag=False
    for i in range(len(refList)):
        if refList[i].ismatch(tmpCla):
            flag=True
            break
    if flag==False:
        print(tmpStr,file=relFile,end='')
'''