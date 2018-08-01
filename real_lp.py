import numpy as np
import random
from sklearn.semi_supervised import label_propagation
import sys
import time
from sklearn.metrics import roc_curve
import matplotlib.pyplot as plt
from math import isnan
SV_type="DEL"
SV_fileName="ngs."+SV_type+".rcd"
SV_file=open(SV_fileName,'w')
simul_Data=np.loadtxt(SV_type)
real_Data=np.loadtxt("ngs_"+SV_type)
myData=np.vstack((simul_Data,real_Data))
X=myData[:,range(1,32)]
y=myData[:,[32]]
list_label_p=[0,5,10,20,30,40,50]
for ind_label_p in range(7):
    label_p=list_label_p[ind_label_p]
    print("label_p:",label_p)
    acc=0
    accl=0
    accnl=0
    prec=0
    precl=0
    precnl=0
    rec=0
    recl=0
    recnl=0
    meantime=0
    for xunhuan in range(10):
        print(xunhuan)
        labels=-np.ones(y.shape[0])
        flag=[]
        noLabelNum=0
        for i in range(y.shape[0]):
            if i<simul_Data.shape[0]:
                labels[i] = y[i, 0]
                flag.append(1)
                continue
            ran = random.randint(0, 99)
            if ran<label_p:
                labels[i]=y[i,0]
                flag.append(1)
            else:
                flag.append(0)
                noLabelNum+=1

        label_spread = label_propagation.LabelSpreading(kernel='knn', alpha=0.8,max_iter=300)
        begin_time=int(time.time()*1000)
        label_spread.fit(X,labels)
    #===============================================
    #Plot ROC curve
        if xunhuan==0:
            prob=label_spread.predict_proba(X[range(simul_Data.shape[0],X.shape[0]),:])
            prob=prob[:,[1]]
            for i in range(len(prob)):
                if isnan(prob[i]):
                    prob[i]=0
            fpr,tpr,thresholds=roc_curve(y[range(simul_Data.shape[0],X.shape[0]),:],prob,pos_label=1)
            #print(len(tpr))
            for i in range(len(fpr)):
                print(fpr[i],file=SV_file,end=' ')
            print('',file=SV_file)
            for i in range(len(tpr)):
                print(tpr[i],file=SV_file,end=' ')
            print('',file=SV_file)
            '''
            plt.plot(fpr,tpr,color='darkorange',lw=2,label=SV_type+' ROC curve')
            plt.xlim([0.0,1.0])
            plt.ylim([0.0,1.05])
            plt.xlabel('False Positive Rate')
            plt.ylabel('True Positive Rate')
            plt.title('ROC')
            plt.legend(loc="lower right")
            plt.show()
            '''
            #sys.stdin.readline()
    #Plot ROC curve END
    #===============================================
        break
        end_time=int(time.time()*1000)
        meantime+=end_time-begin_time
        rel=label_spread.transduction_
        tpNumNoLabels=0
        tpNumLabels=0
        tpNum=0
        pNum=0
        tp=0
        tpls=0
        tpnls=0
        tpl=0
        tpnl=0
        prelnum=0
        prelnuml=0
        prelnumnl=0
        for i in range(y.shape[0]):
            if rel[i]==1:
                prelnum+=1
                if flag[i]==0:
                    prelnumnl+=1
                else:
                    prelnuml+=1
            if y[i,0]==1:
                pNum+=1
                if flag[i]==0:
                    tpnls+=1
                else:
                    tpls+=1
            if rel[i]==1 and y[i,0]==1:
                tp+=1
                if flag[i]==0:
                    tpnl+=1
                else:
                    tpl+=1
            if flag[i]==0 and rel[i]==y[i,0]:
                tpNumNoLabels+=1
            if flag[i]==1 and rel[i]==y[i,0]:
                tpNumLabels+=1
            if rel[i]==y[i,0]:
                tpNum+=1
        accnl+=tpNumNoLabels/noLabelNum
        accl+=tpNumLabels/(y.shape[0]-noLabelNum)
        acc+=tpNum/y.shape[0]
        recnl+=tpnl/tpnls
        recl+=tpl/tpls
        rec+=tp/pNum
        precnl+=tpnl/prelnumnl
        precl+=tpl/prelnuml
        prec+=tp/prelnum
    print("Accuracy of no labels:",accnl/10)
    print("Accuracy of labels:",accl/10)
    print("Accuracy:",acc/10)
    print("Recall of no labels:",recnl/10)
    print("Recall of labels:",recl/10)
    print("Recall:",rec/10)
    print("Precision of no labels:",precnl/10)
    print("Precision of labels:",precl/10)
    print("Precision:",prec/10)
    print("Time used:",meantime/10)


