readLineF<- function(fileLink){
  line <- readLines(fileLink,1)
  line <- strsplit(line,' ')
  line <- unlist(line)
  return(as.numeric(line))
}

library(ggplot2)
SV_type<-"DEL"
label_p<-c('5','10','20','30','40','50')
mlmethod<-c("label spreading","svm","randomforest")
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
all_data<-data.frame(p_data,auc_data,method_data)
all_data$method_data<-factor(all_data$method_data,levels=(c("svm","label spreading","randomforest")))
all_data$p_data<-factor(all_data$p_data,levels=(label_p))
bb2<-ggplot(data=all_data,aes(x=p_data,y=auc_data,fill=method_data,width=0.6))+
    geom_bar(stat="identity",position=position_dodge(width=0.67))+
    xlab("label percentage(%)")+
    ylab("AUC")+
    labs(fill='',title="AUC of deletions","labeled")+
    theme(plot.title = element_text(hjust=0.5),
          legend.position = c(1,1),
          legend.justification=c(0, 1),
          legend.key.width=unit(1, "lines"), 
          plot.margin = unit(c(1, 8, 0.5, 0.5), "lines"))+
    scale_y_continuous(expand = c(0,0),limits=c(0,1))
p_data<-c(5,10,20,30,40,50)
all_data<-data.frame(p_data,auc_data,method_data)
bb2<-ggplot()+
    geom_line(data=all_data,aes(x=p_data,y=auc_data,colour=method_data))+
    xlab("label percentage(%)")+
    ylab("AUC")+
    labs(colour='',title="AUC of deletions","labeled")+
    theme(plot.title = element_text(hjust=0.5),
        legend.position = c(1,1),
        legend.justification=c(0, 1),
        legend.key.width=unit(1, "lines"), 
        plot.margin = unit(c(1, 8, 0.5, 0.5), "lines"))
    #scale_y_continuous(limits=c(5,50))1


print(bb2)



