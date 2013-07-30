d <- read.table(file="/home/evan/Documents/chicago/dssg-landbank-project/analysis/CA_ptype_median_bldg_size.csv",header = TRUE,sep=",")
d1 <- read.table(file="/home/evan/Documents/chicago/dssg-landbank-project/analysis/CA_ptype_median_bldg_psf.csv",header = TRUE,sep=",")
d2 <- read.table(file="/home/evan/Documents/chicago/dssg-landbank-project/analysis/CA_ptype_median_land_size.csv",header = TRUE,sep=",")
d3 <- read.table(file="/home/evan/Documents/chicago/dssg-landbank-project/analysis/CA_ptype_median_land_psf.csv",header = TRUE,sep=",")

d <- data.frame(d,d1[,3],d2[,3],d3[,3])

community_area <- str_trim(d1[,1],side = "both")

d <- data.frame(community_area,d[,-1])
d <- adply(d,1,transform,singleFamSellPrice=((sqft_bldg_11*bldg_assmt_11_psf)+(sqft_land_11*land_assmt_11_psf)))

p <- ggplot(data = d,aes(x=PTYOE2011,y=singleFamSellPrice))+geom_boxplot()
