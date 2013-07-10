
d <- read.table(file="~/Documents/chicago/dssg-landbank-project/analysis/testfc.csv",header=FALSE,sep=",",)
library("stringr")
library("zoo")
createString <- function(x){
  createString <- paste(substr(as.character(x),1,4),substr(as.character(x),5,5),sep="-")
  
  return(createString)
}

community_area <- str_trim(d[,1],side = "both")
d<-data.frame(d[,2],community_area,d[,3])
colnames(d)[c(1,3)] <- c("quarterly num","foreclosure")
head(d)
dateStrings <- unlist(lapply(d[,1],createString))
yyyyq_doc <- as.yearqtr(dateStrings)

yyyyq_doc_date=as.Date(yyyyq_doc)

d <- data.frame(d[,1],yyyyq_doc_date,d[,2:3])
head(d)
## =======
## d <- data.frame(d[,1],yyyyq_doc,d[,2:3])
## yyyyq_doc_date <- as.Date(yyyyq_doc)
## d<- data.frame(d[,1],yyyyq_doc_date,d[,2:4])
## >

library(ggplot2)
p <- ggplot(data=d[d$community_area=='Albany Park',], aes(yyyyq_doc_date,foreclosure))+geom_line()
print(p)
