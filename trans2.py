import sys
import io
import re
from collections import defaultdict

allDel={}


class mydel():
    types=defaultdict(int)
    typesId=1
    def __init__(self,tmpstr,myid):
        #print(tmpstr)
        li=tmpstr.split("\t")
        self.chr=li[0]
        self.st=int(li[1])
        self.ed=int(li[2])
        li2=li[3].split(",")
        self.seq_type=[]
        self.seq_dis=self.ed-self.st+1
        self.seq_positive=[]
        self.seq_negative=[]
        self.seq_flag=[]
        self.id=myid
        for i in range(0,len(li2)):
            if self.types[li2[i]]==0:
                self.addtype(li2[i])
            self.seq_type.append(self.types[li2[i]])
        li2=li[4].split(",")
        for i in range(0,len(li2)):
            self.seq_positive.append(int(li2[i].split("+")[0]))
            self.seq_negative.append(int(li2[i].split("+")[1][:-1]))
        '''
        li2=li[5].split(",")
        for i in range(0,len(li2)):
            if i==0:
                self.seq_dis.append(int(li2[i]))
            else:
                self.seq_dis.append(int(li2[i])-int(li2[i-1]))
            if i==len(li2)-1:
                self.seq_len=int(li2[i])-int(li2[0])
        '''
    def printme(self,mytype):
        rel=str(self.id)+' '
        findflag=0
        for i in range(0,len(self.seq_type)):
            tmpflag=0
            if self.seq_positive[i]>self.seq_negative[i]:
                tmpflag=1
            elif self.seq_positive[i]<self.seq_negative[i]:
                tmpflag=2
            if tmpflag>0 and findflag==0:
                for j in range(0,i):
                    self.seq_flag[j]=tmpflag
            if tmpflag>0:
                findflag=tmpflag
                self.seq_flag.append(tmpflag)
            else:
                self.seq_flag.append(findflag)
        for i in range(0,10):
            if i<len(self.seq_type):
                if i==0:
                    rel=rel+str(self.seq_type[i])+' '+str(self.ed-self.st)+' '+str(self.seq_flag[i])+' '+str(self.seq_negative[i]+self.seq_positive[i])+' '
                else:
                    rel=rel+str(self.seq_type[i])+' '+str(self.seq_flag[i])+' '+str(self.seq_negative[i]+self.seq_positive[i])+' '
            else:
                rel=rel+"0 0 0 "
        rel=rel+str(mytype)
        return rel
    @classmethod
    def addtype(cls,tmpstr):
        cls.types[tmpstr]=cls.typesId
        cls.typesId=cls.typesId+1

notDelFile=open("ngs2.NotDUP")
notDelRel=open("ngs2.not.DUP.rel","w")
delFile=open("ngs2.DUP")
delRel=open("ngs2.DUP.rel","w")
myid=0
while 1:
    tmpstr=notDelFile.readline()
    if tmpstr=='':
        break
    if tmpstr.split('\t')[2]=='-':
        continue
    myid=myid+1
    tmpmydel=mydel(tmpstr,myid)
    if len(tmpmydel.seq_type)>10:
        continue
    print(tmpmydel.printme(0),file=notDelRel)
myid=0
while 1:
    tmpstr = delFile.readline()
    if tmpstr == '':
        break
    if tmpstr.split('\t')[2]=='-':
        continue
    myid=myid+1
    tmpmydel = mydel(tmpstr,myid)
    if len(tmpmydel.seq_type) > 10:
        continue
    print(tmpmydel.printme(1), file=delRel)