neighb4comp <- function(w=38,x=12,y=24,z=18,d)
    {
        data_mask <- ((d$community_area == levels(d[['community_area']])[w]) |
                      (d$community_area == levels(d[['community_area']])[x]) |
            (d$community_area == levels(d[['community_area']])[y]) |
            (d$community_area == levels(d[['community_area']])[z]))
        chart_title <- paste("Foreclosures over
 time in ",
                             levels(d[['community_area']])[w],", ",
                                        levels(d[['community_area']])[x],", ",
                                        levels(d[['community_area']])[y],
                                        " and ",
                                        levels(d[['community_area']])[z],
                                        sep="")
                                        
        p <- ggplot(data=d[data_mask,],aes(yyyyq_doc_date,foreclosure,colour=community_area))+geom_line()+ggtitle(chart_title)+theme_bw()
        ggsave(filename = "/home/evan/Documents/chicago/dssg-landbank-project/analysis/foreclosure_graphs/fourSample.pdf")
        return(p)
                    
    }
