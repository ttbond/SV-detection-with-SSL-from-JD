import sys
import re
sourceFile=open("ngsValidatedINV.info")
relFile=open("ngs.INV","w")
id=1
while 1:
    print(id)
    tmpStr=sourceFile.readline()
    if tmpStr=='':
        break
    tmpStr=tmpStr.split("\t")
    relStr=''+tmpStr[0]+'\t'+tmpStr[1]+'\t'+tmpStr[2]+'\t'
    tmpStr=tmpStr[4].split(';')
    flag = False
    for strs in tmpStr:
        sonStr = strs.split("=")
        if sonStr[0] == "Pattern":
            relStr = relStr + sonStr[1].split('\n')[0] + '\t'
            flag = True
    if flag == False:
        print(id, "Pattern error")
    flag=False
    for strs in tmpStr:
        sonStr=strs.split("=")
        if sonStr[0]=="Ori":
            relStr=relStr+sonStr[1].split('\n')[0]+'\t'
            flag=True
    if flag==False:
        print(id,"Ori error")
    '''
    flag=False
    for strs in tmpStr:
        sonStr=strs.split("=")
        if sonStr[0]=="Pos":
            relStr=relStr+sonStr[1].split('\n')[0]
            flag=True
    if flag==False:
        print(id,"Pos error")
    '''
    print(relStr,file=relFile)
    id+=1


