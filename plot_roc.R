library(ggplot2)
DEL_data=read.table("DEL.rcd",header=FALSE)
DEL_data<-as.data.frame(DEL_data)
DUP_data=read.table("DUP.rcd",header=FALSE)
DUP_data<-as.data.frame(DUP_data)
INV_data=read.table("INV.rcd",header=FALSE)
INV_data<-as.data.frame(INV_data)
x_data=c(t(DEL_data[2,]),t(DUP_data[2,]),t(INV_data[2,]))
y_data=c(t(DEL_data[1,]),t(DUP_data[1,]),t(INV_data[1,]))
type_data=c(rep("DEL",length(DEL_data)),rep("DUP",length(DUP_data)),rep("INV",length(INV_data)))
all_data=data.frame(x_data,y_data,type_data)
all_data<-as.data.frame(all_data)
bb<-ggplot()+
  geom_line(data=all_data,aes(x=all_data[,2],y=all_data[,1],colour=all_data[,3]))+
  xlab("TPR")+
  ylab("FPR")+
  labs(colour="SV type")
