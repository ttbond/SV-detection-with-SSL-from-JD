library(ggplot2)
dataFile <- file("DUP.rcd","r")
label_p=c('5','10','20','30','40','50')
x_data<-numeric()
y_data<-numeric()
type_data<-numeric()
for(ii in 1:6){
  line <- readLines(dataFile,n=1)
  line <- strsplit(line,' ')
  line <- unlist(line)
  print(length(line))
  for(i in 1:length(line)){
    x_data<-c(x_data,as.numeric(line[i]))
  }
  line <- readLines(dataFile,n=1)
  line <- strsplit(line,' ')
  line <- unlist(line)
  for(i in 1:length(line)){
    y_data<-c(y_data,as.numeric(line[i]))
  }
  type_data<-c(type_data,rep(label_p[ii],length(line)))
}
close(dataFile)
x_data<-unlist(x_data)
y_data<-unlist(y_data)
type_data<-unlist(type_data)
all_data=data.frame(x_data,y_data,type_data)
all_data$type_data<-factor(all_data$type_data,levels=label_p)
bb<-ggplot()+
  geom_line(data=all_data,aes(x=all_data[,1],y=all_data[,2],colour=all_data[,3]))+
  xlab("FPR")+
  ylab("TPR")+
  labs(colour="Label Percentage",title="DUP ROC curve of simulated data")+
  theme(plot.title = element_text(hjust=0.5))
bb
