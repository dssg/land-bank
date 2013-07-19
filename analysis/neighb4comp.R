neighb4comp <- function(w=38,x=12,y=24,z=18,seriesFlag=0,d)
    {
        data_mask <- ((d$community_area == levels(d[['community_area']])[w]) |
                      (d$community_area == levels(d[['community_area']])[x]) |
            (d$community_area == levels(d[['community_area']])[y]) |
            (d$community_area == levels(d[['community_area']])[z]))

switch(seriesFlag,
    T1={depVal <- "Mortgage Count"
        graph_path <- "mortgageCounts"
    },
    T2={depVal <- "Foreclosure Count"
        graph_path <- "foreclosure_graphs"
    },
    T3={depVal <- "Mortgage Median Value"
        graph_path <- "mortgageMedianSize"
    },
    stop("Enter something that switches me")
)
        chart_title <- paste(depVal, " over
 time in ",
                             levels(d[['community_area']])[w],", ",
                                        levels(d[['community_area']])[x],", ",
                                        levels(d[['community_area']])[y],
                                        " and ",
                                        levels(d[['community_area']])[z],
                                        sep="")
switch(seriesFlag,
        T1={p <- ggplot(data=d[data_mask,],aes(yyyyq_doc_date,mortgage,colour=community_area))+geom_line()+ggtitle(chart_title)+theme_bw()
        },
       T2={p <- ggplot(data=d[data_mask,],aes(yyyyq_doc_date,foreclosure,colour=community_area))+geom_line()+ggtitle(chart_title)+theme_bw()
       },
       T3={p <- ggplot(data=d[data_mask,],aes(yyyyq_doc_date,mortgage_med_size,colour=community_area))+geom_line()+ggtitle(chart_title)+theme_bw()+scale_y_continuous(labels = comma)
        },
        stop("Enter something that switches me")
)
       
        base_path="/home/evan/Documents/chicago/dssg-landbank-project/analysis/"
        full_path <- paste(base_path,graph_path,sep="/")
        ggsave(filename = paste(full_path,"/fourSample.pdf",sep=""))
        return(p)
                    
    }
