library(ggplot2)
dataFile <- file("ngs.INV.rcd","r")
label_p=c('0','5','10','20','30','40','50')
x_data<-numeric()
y_data<-numeric()
type_data<-numeric()
tmp_len<-numeric()
for(ii in 1:length(label_p)){
  line <- readLines(dataFile,n=1)
  line <- strsplit(line,' ')
  line <- unlist(line)
  print(length(line))
  tmp_len<-c(tmp_len,length(line))
  for(i in 1:length(line)){
    x_data<-c(x_data,as.numeric(line[i]))
  }
  line <- readLines(dataFile,n=1)
  line <- strsplit(line,' ')
  line <- unlist(line)
  for(i in 1:length(line)){
    y_data<-c(y_data,as.numeric(line[i]))
  }
}
line <- readLines(dataFile,n=1)
line <- strsplit(line,' ')
line <- unlist(line)
close(dataFile)
label_p=paste(label_p,"AUC=")
label_p=paste(label_p,substr(line,0,6),sep='')
for(i in 1:length(tmp_len)){
  type_data <- c(type_data,rep(label_p[i],tmp_len[i]))
}
x_data<-unlist(x_data)
y_data<-unlist(y_data)
type_data<-unlist(type_data)
all_data=data.frame(x_data,y_data,type_data)
all_data$type_data<-factor(all_data$type_data,levels=label_p)
bb<-ggplot()+
  geom_line(data=all_data,aes(x=all_data[,1],y=all_data[,2],colour=all_data[,3]))+
  xlab("FPR")+
  ylab("TPR")+
  labs(colour="Label Percentage",title="INV ROC curve of combined data")+
  theme(plot.title = element_text(hjust=0.5))
bb
