readLineF<- function(fileLink){
  line <- readLines(fileLink,1)
  line <- strsplit(line,' ')
  line <- unlist(line)
  return(as.numeric(line))
}

library(ggplot2)
sv_type<-"DUP"
dataFile <- file(paste("ngs2",sv_type,"rcd",sep='.'),"r")
label_p=c('5','10','20','30','40','50')
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
auc_data<-readLineF(dataFile)
close(dataFile)
#label_p=paste(label_p,"AUC=")
#label_p=paste(label_p,substr(line,0,6),sep='')
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
  labs(colour="label percentage(%)",title="duplication of real data")+
  theme(plot.title = element_text(hjust=0.5),legend.position = c(0.18,0.33),legend.key.width=unit(2,'cm'))+
  scale_y_continuous(limits = c(0,1))


label_type<-label_p
auc_part<-data.frame(label_p,auc_data,label_type)
auc_part$label_type<-factor(auc_part$label_type,levels=(label_p))
auc_part$label_p<-factor(auc_part$label_p,levels=(label_p))
bb22<-ggplot(data=auc_part,aes(x=label_p,y=auc_data,fill=label_type))+
  geom_bar(stat="identity",position='dodge',width=0.7)+
  coord_cartesian(ylim=c(0.8,1)) +
  theme(axis.title.x=element_blank(),
        axis.text.x=element_blank(),
        axis.ticks.x=element_blank(),
        axis.line.x=element_blank(),
        legend.position = "none")+
  ylab("AUC")+
  scale_y_continuous(expand = c(0,0))


library(viridis)
left_part<-ggdraw()+
  draw_plot(bb,0,0,1,1)+
  draw_plot(bb22,0.52,0.23,0.4,0.4)
print(left_part)

