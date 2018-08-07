readLineF<- function(fileLink){
  line <- readLines(fileLink,1)
  line <- strsplit(line,' ')
  line <- unlist(line)
  return(as.numeric(line))
}

library(ggplot2)
SV_type<-c("DEL","DUP","INS","INV")
label_p<-c(5,10,20,30,40,50)
sv_data<-numeric()
auc_data<-numeric()
tar_p=50
for(sv in SV_type){
  dataFile <- file(paste("ngs.compare.",sv,".rcd",sep=''),"r")
  for(i in 1:3){
    line <- readLineF(dataFile)
    print(line)
    sv_data<-c(sv_data,sv)
    auc_data<-c(auc_data,line[which(label_p==tar_p)])
  }
  close(dataFile)
}
method_data<-rep(c("lp","svm","randomforest"),4)
all_data=data.frame(sv_data,auc_data,method_data)
all_data$method_data<-factor(all_data$method_data,levels=(c("svm","lp","randomforest")))
bb<-ggplot(data=all_data,aes(x=sv_data,y=auc_data,fill=method_data))+
    geom_bar(stat="identity",position='dodge')+
    xlab("SV type")+
    ylab("AUC value")+
    labs(fill="Method",title=paste("AUC of Simulated Data with",paste(as.character(tar_p),'%',sep=''),"labeled"))+
    theme(plot.title = element_text(hjust=0.5))
print(bb)



