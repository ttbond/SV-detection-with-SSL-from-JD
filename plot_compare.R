library(ggplot2)
SV_type="DEL"
dataFile <- file(paste("ngs2.compare.",SV_type,".rcd",sep=''),"r")
label_p<-c(3,5,10,20,30,40,50)
x_data<-numeric()
y_data<-numeric()
x_data<-c(label_p,label_p,label_p)
type_data<-numeric()
line <- readLines(dataFile,n=1)
line <- strsplit(line,' ')
line <- unlist(line)
y_data<-as.numeric(line)
line <- readLines(dataFile,n=1)
line <- strsplit(line,' ')
line <- unlist(line)
y_data <- c(y_data,as.numeric(line))
line <- readLines(dataFile,n=1)
line <- strsplit(line,' ')
line <- unlist(line)
close(dataFile)
y_data <- c(y_data,as.numeric(line))
type_data<-c(rep("lp",length(label_p)),rep("SVM",length(label_p)),rep("RF",length(label_p)))
all_data=data.frame(x_data,y_data,type_data)
bb<-ggplot()+
  geom_line(data=all_data,aes(x=all_data[,1],y=all_data[,2],colour=all_data[,3]))+
  xlab("Label Percentage")+
  ylab("AUC")+
  labs(colour="Method",title=paste(SV_type,"AUC of Simulated Data"))+
  theme(plot.title = element_text(hjust=0.5))
  
print(bb)
