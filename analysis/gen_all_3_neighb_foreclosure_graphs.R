gen_all_3_neighb_forclosure <- function(d)
    {
        unique_ca <- length(levels(d[['community_area']]))
        for(i in 1:(unique_ca-2))
            {
                for(j in (i+1):(unique_ca-1))
                    {
                      for(k in (j+1):unique_ca)
                          {
                              cat("i=",i,"j=",j,"k=",k,"\n")
                              p1 <- neighb3comp(i,j,k,d)
                              chart_path <-"~/dssg-landbank-project/analysis/foreclosure_graphs"
                              firstG <- sub(' ',"_",levels(d[['community_area']])[i])
                              secG <- sub(' ',"_",levels(d[['community_area']])[j])
                              thirdG<- sub(' ',"_",levels(d[['community_area']])[k])
                              chart_title <- paste("Foreclosures",
                                                              firstG,
                                                              secG,
                                                              thirdG,
                                                              sep="_")
                              cat("chart_title=",chart_title,"\n")
                              cat("chart_path=",chart_path,"\n")
                              prefix=paste(chart_path,chart_title,sep="/")
                              suffix="pdf"
                              full_name <- paste(prefix,suffix,sep=".")
                              cat("full_name=",full_name,"\n")                              
                              ggsave(filename=full_name)
                          }
                  
                  }
            }
    }
