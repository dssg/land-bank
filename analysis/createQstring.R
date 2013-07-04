createString <- function(x){
        createString <- paste(substr(as.character(x),1,4),substr(as.character(x),5,5),sep="-")

        return(createString)
    }
