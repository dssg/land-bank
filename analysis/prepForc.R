switch(seriesFlag,
       T1={d <- read.table(file="single_fam_mort_count_trans_by_qtr.csv",header = TRUE,sep=",")
       },
       T2={d <- read.table(file="/home/evan/Documents/chicago/dssg-landbank-project/analysis/single_family_defaults_by_ca_over_time.csv",header = FALSE,sep = ",")
       },
       T3={d <- read.table(file="single_fam_mort_median_trans_by_qtr.csv",header = TRUE,sep=",")
       },
        stop("Enter something that switches me")
)
library("stringr")
library("zoo")
createString <- function(x){
  createString <- paste(substr(as.character(x),1,4),substr(as.character(x),5,5),sep="-")
  
  return(createString)
}
community_area <- str_trim(d[,1],side = "both")
d[d['PTYPE2011']=='SINGLE FAMILY',]
d<-data.frame(d[,2],community_area,d[,3])
switch(seriesFlag,
    T1={colnames(d)[c(1,3)] <- c("quarterly num","mortgage")
    },
    T2={colnames(d)[c(1,3)] <- c("quarterly num","foreclosure")
    },
    T3={colnames(d)[c(1,3)] <- c("quarterly num","mortgage_med_size")        
    },
        stop("Enter something that switches me")
)
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


switch(seriesFlag,    
    T1={p <- ggplot(data=d[d$community_area=='Albany Park',], aes(yyyyq_doc_date,mortgage))+geom_line()
    },
    T2={p <- ggplot(data=d[d$community_area=='Albany Park',], aes(yyyyq_doc_date,foreclosure))+geom_line()
    },
    T3={p <- ggplot(data=d[d$community_area=='Albany Park',], aes(yyyyq_doc_date,mortgage_med_size))+geom_line()
    },
    stop("Enter something that switches me")
)

print(p)
