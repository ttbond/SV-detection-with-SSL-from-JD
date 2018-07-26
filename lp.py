import numpy as np
import random
from sklearn.semi_supervised import label_propagation
from sklearn.svm import SVC
import sys
import time
myData=np.loadtxt("DUP")
X=myData[:,range(1,32)]
y=myData[:,[32]]
label_p=50
acc=0
accl=0
accnl=0
prec=0
precl=0
precnl=0
rec=0
recl=0
recnl=0

svm_acc=0
svm_accl=0
svm_accnl=0
svm_prec=0
svm_precl=0
svm_precnl=0
svm_rec=0
svm_recl=0
svm_recnl=0

meantime=0
svm_meantime=0
for xunhuan in range(10):
    print(xunhuan)
    labels=-np.ones(y.shape[0])
    flag=[]
    noLabelNum=0
    for i in range(y.shape[0]):
        ran=random.randint(0,99)
        if ran<label_p:
            labels[i]=y[i,0]
            flag.append(1)
        else:
            flag.append(0)
            noLabelNum+=1
    label_spread = label_propagation.LabelSpreading(kernel='knn', alpha=0.8,max_iter=300)
    begin_time=int(time.time()*1000)
    label_spread.fit(X,labels)
    end_time=int(time.time()*1000)
    meantime+=end_time-begin_time
    rel=label_spread.transduction_
    svm_train_x=np.delete(X,np.where(np.array(flag)==0),axis=0)
    svm_train_y=np.delete(y,np.where(np.array(flag)==0))
    begin_time = int(time.time() * 1000)
    svm_clf = SVC()
    svm_clf.fit(svm_train_x,svm_train_y)
    svm_rel=svm_clf.predict(X)
    end_time = int(time.time() * 1000)
    svm_meantime=end_time-begin_time
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
#====================================================
#svm statistical data
    tpNumNoLabels = 0
    tpNumLabels = 0
    tpNum = 0
    pNum = 0
    tp = 0
    tpls = 0
    tpnls = 0
    tpl = 0
    tpnl = 0
    prelnum = 0
    prelnuml = 0
    prelnumnl = 0
    for i in range(y.shape[0]):
        if svm_rel[i] == 1:
            prelnum += 1
            if flag[i] == 0:
                prelnumnl += 1
            else:
                prelnuml += 1
        if y[i, 0] == 1:
            pNum += 1
            if flag[i] == 0:
                tpnls += 1
            else:
                tpls += 1
        if svm_rel[i] == 1 and y[i, 0] == 1:
            tp += 1
            if flag[i] == 0:
                tpnl += 1
            else:
                tpl += 1
        if flag[i] == 0 and svm_rel[i] == y[i, 0]:
            tpNumNoLabels += 1
        if flag[i] == 1 and svm_rel[i] == y[i, 0]:
            tpNumLabels += 1
        if svm_rel[i] == y[i, 0]:
            tpNum += 1
    svm_accnl += tpNumNoLabels / noLabelNum
    svm_accl += tpNumLabels / (y.shape[0] - noLabelNum)
    svm_acc += tpNum / y.shape[0]
    svm_recnl += tpnl / tpnls
    svm_recl += tpl / tpls
    svm_rec += tp / pNum
    #
    # svm_precnl += tpnl / prelnumnl
    svm_precl += tpl / prelnuml
    svm_prec += tp / prelnum
#svm statitical data END
#=====================================================
print("Accuracy of no labels:",accnl/10,svm_accnl/10)
print("Accuracy of labels:",accl/10,svm_accl/10)
print("Accuracy:",acc/10,svm_acc/10)
print("Recall of no labels:",recnl/10,svm_recnl/10)
print("Recall of labels:",recl/10,svm_recl/10)
print("Recall:",rec/10,svm_rec/10)
print("Precision of no labels:",precnl/10,svm_precnl/10)
print("Precision of labels:",precl/10,svm_precl/10)
print("Precision:",prec/10,svm_prec/10)
print("Time used:",meantime/10)
print("SVMTimeUsed:",svm_meantime/10)
rel_file=open("pl_rel.dat","w")
print(accnl/10,svm_accnl/10,file=rel_file)
print(accl/10,svm_accl/10,file=rel_file)
print(acc/10,svm_acc/10,file=rel_file)
print(recnl/10,svm_recnl/10,file=rel_file)
print(recl/10,svm_recl/10,file=rel_file)
print(rec/10,svm_rec/10,file=rel_file)
print(precnl/10,svm_precnl/10,file=rel_file)
print(precl/10,svm_precl/10,file=rel_file)
print(prec/10,svm_prec/10,file=rel_file)
