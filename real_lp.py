import numpy as np
import random
from sklearn.semi_supervised import label_propagation
import sys
import time
from sklearn.metrics import auc
from sklearn.metrics import roc_curve
import matplotlib.pyplot as plt
from math import isnan
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
SV_type="DUP"
SV_fileName="ngs2."+SV_type+".rcd"
SV_file=open(SV_fileName,'w')
compare_file=open("ngs2.compare."+SV_type+".rcd",'w')
#simul_Data=np.loadtxt(SV_type)
real_Data=np.loadtxt("ngs2_"+SV_type)


#myData=np.vstack((simul_Data,real_Data))
#myData=simul_Data
myData=real_Data

X=myData[:,range(1,32)]
y=myData[:,[32]]
list_label_p=[5,10,20,30,40,50]
myAUC=np.array([])
svm_AUC=np.array([])
rf_AUC=np.array([])
total_lp_acc=[]
total_svm_acc=[]
total_rf_acc=[]
for ind_label_p in range(len(list_label_p)):
    prob = np.array([])
    rel_y = np.array([])
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

    #===================================
    #SVM relative data
    svm_acc = 0
    svm_accl = 0
    svm_accnl = 0
    svm_prec = 0
    svm_precl = 0
    svm_precnl = 0
    svm_rec = 0
    svm_recl = 0
    svm_recnl = 0
    #SVM relative data end
    #===================================

    # ===================================
    # RF relative data
    rf_acc = 0
    rf_accl = 0
    rf_accnl = 0
    rf_prec = 0
    rf_precl = 0
    rf_precnl = 0
    rf_rec = 0
    rf_recl = 0
    rf_recnl = 0
    # RF relative data end
    # ===================================

    for xunhuan in range(10):
        print(xunhuan)
        labels=-np.ones(y.shape[0])
        flag=[]
        noLabelNum=0
        for i in range(y.shape[0]):
            '''
            if i<simul_Data.shape[0]:
                labels[i] = y[i, 0]
                flag.append(1)
                continue
            '''
            ran = random.randint(0, 99)
            if ran<label_p:
                labels[i]=y[i,0]
                flag.append(1)
            else:
                flag.append(0)
                noLabelNum+=1
        print("flag len:",len(np.where(np.array(flag)==0)[0]))
        label_spread = label_propagation.LabelSpreading(kernel='knn', alpha=0.8,max_iter=300)
        begin_time=int(time.time()*1000)
        label_spread.fit(X,labels)

    #===============================================
    #Plot ROC curve
        tmpFlag = np.array(flag)
        tmp_prob = label_spread.predict_proba(X[np.where(tmpFlag == 0)[0], :])
        tmprel = label_spread.predict(X)
        if xunhuan == 0:
            prob = tmp_prob[:, [1]]
            rel_y = y[np.where(tmpFlag == 0)[0], :]
        else:
            prob = np.vstack((prob, tmp_prob[:, [1]]))
            rel_y = np.vstack((rel_y, y[np.where(tmpFlag == 0)[0], :]))
        for i in range(len(prob)):
            if isnan(prob[i]):
                prob[i] = 0
    #Plot ROC curve END
    #===============================================

    #===============================================
    #statistic lp relative targets
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
    #statistic lp relative targets end
    #=========================================================

    
    # ====================================================
    # svm statistical data
        svm_train_x = np.delete(X, np.where(np.array(flag) == 0), axis=0)
        svm_train_y = np.delete(y, np.where(np.array(flag) == 0))
        begin_time = int(time.time() * 1000)
        svm_clf = SVC(probability=True)
        svm_clf.fit(svm_train_x, svm_train_y)
        svm_rel = svm_clf.predict(X)
        end_time = int(time.time() * 1000)
        svm_meantime = end_time - begin_time
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
        # svm_precnl += tpnl / prelnumnl
        svm_precl += tpl / prelnuml
        svm_prec += tp / prelnum
        tmp_prob = svm_clf.predict_proba(X[np.where(tmpFlag == 0)[0], :])
        for i in range(len(tmp_prob)):
            if isnan(tmp_prob[i,0]):
                tmp_prob[i,0] = 0
        if xunhuan == 0:
            svm_prob = tmp_prob[:, [1]]
        else:
            svm_prob = np.vstack((svm_prob, tmp_prob[:, [1]]))
    # svm statitical data END
    # =====================================================

    # ====================================================
    # RF statistical data
        svm_train_x = np.delete(X, np.where(np.array(flag) == 0), axis=0)
        svm_train_y = np.delete(y, np.where(np.array(flag) == 0))
        begin_time = int(time.time() * 1000)
        rf_clf = RandomForestClassifier(n_estimators=1000)
        rf_clf.fit(svm_train_x, svm_train_y)
        rf_rel = rf_clf.predict(X)
        end_time = int(time.time() * 1000)
        svm_meantime = end_time - begin_time
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
            if rf_rel[i] == 1:
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
            if rf_rel[i] == 1 and y[i, 0] == 1:
                tp += 1
                if flag[i] == 0:
                    tpnl += 1
                else:
                    tpl += 1
            if flag[i] == 0 and rf_rel[i] == y[i, 0]:
                tpNumNoLabels += 1
            if flag[i] == 1 and rf_rel[i] == y[i, 0]:
                tpNumLabels += 1
            if rf_rel[i] == y[i, 0]:
                tpNum += 1
        rf_accnl += tpNumNoLabels / noLabelNum
        rf_accl += tpNumLabels / (y.shape[0] - noLabelNum)
        rf_acc += tpNum / y.shape[0]
        rf_recnl += tpnl / tpnls
        rf_recl += tpl / tpls
        rf_rec += tp / pNum
        # svm_precnl += tpnl / prelnumnl
        rf_precl += tpl / prelnuml
        rf_prec += tp / prelnum
        tmp_prob = rf_clf.predict_proba(X[np.where(tmpFlag == 0)[0]])
        for i in range(len(tmp_prob)):
            if isnan(tmp_prob[i,0]):
                print(tmp_prob[i,0])
                tmp_prob[i,0] = 0
        if xunhuan == 0:
            rf_prob = tmp_prob[:, [1]]
        else:
            rf_prob = np.vstack((rf_prob, tmp_prob[:, [1]]))
        print("length rel_y:",len(rel_y))
        print("length svm_prob:",len(svm_prob))
        print("length rf_prob:", len(rf_prob))

    # RF statitical data END
    # =====================================================


    fpr, tpr, thresholds = roc_curve(rel_y, prob, pos_label=1)
    tmpAUC=auc(fpr,tpr,reorder=False)
    myAUC=np.append(myAUC,tmpAUC)


    fpr, tpr, thresholds = roc_curve(rel_y, svm_prob, pos_label=1)
    tmpAUC = auc(fpr, tpr, reorder=False)
    svm_AUC = np.append(svm_AUC, tmpAUC)
    fpr, tpr, thresholds = roc_curve(rel_y, rf_prob, pos_label=1)
    tmpAUC = auc(fpr, tpr, reorder=False)
    rf_AUC = np.append(rf_AUC, tmpAUC)


    for i in range(len(fpr)):
        print(fpr[i], file=SV_file, end=' ')
    print('', file=SV_file)
    for i in range(len(tpr)):
        print(tpr[i], file=SV_file, end=' ')
    print('', file=SV_file)
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
    total_lp_acc.append(accnl/10)
    total_svm_acc.append(svm_accnl/10)
    total_rf_acc.append(rf_accnl/10)

for i in range(len(myAUC)):
    print(myAUC[i],file=SV_file,end=' ')
print('',file=SV_file)


for i in myAUC:
    print(i,file=compare_file,end=' ')
print('',file=compare_file)
for i in svm_AUC:
    print(i,file=compare_file,end=' ')
print('',file=compare_file)
for i in rf_AUC:
    print(i,file=compare_file,end=' ')
print('',file=compare_file)

