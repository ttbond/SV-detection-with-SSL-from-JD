readLineF<- function(fileLink){
  line <- readLines(fileLink,1)
  line <- strsplit(line,' ')
  line <- unlist(line)
  return(as.numeric(line))
}

library(ggplot2)
SV_type<-"DEL"
label_p<-c('5','10','20','30','40','50')
mlmethod<-c("lp","svm","randomforest")
p_data<-numeric()
auc_data<-numeric()
method_data<-numeric()
dataFile <- file(paste("ngs2.compare.",SV_type,".rcd",sep=''),"r")
for(j in 1:length(mlmethod)){
  line <- readLineF(dataFile)
  auc_data <- c(auc_data,line)
  method_data<-c(method_data,rep(mlmethod[j],length(line)))
  p_data<-c(p_data,label_p)
}
close(dataFile)
all_data=data.frame(p_data,auc_data,method_data)
all_data$method_data<-factor(all_data$method_data,levels=(c("svm","lp","randomforest")))
all_data$p_data<-factor(all_data$p_data,levels=(label_p))
bb<-ggplot(data=all_data,aes(x=p_data,y=auc_data,fill=method_data))+
    geom_bar(stat="identity",position='dodge')+
    xlab("label percentage")+
    ylab("AUC value")+
    labs(fill="Method",title="AUC of Real Data with","labeled")+
    theme(plot.title = element_text(hjust=0.5))
print(bb)



