d=read.csv('FirstEmergence.csv');head(d)
library(ggplot2)
ggplot(data=d,aes(x=순위,y=gap))+geom_point(aes(colour=d$왕명), na.rm=TRUE)
