## daymet_tile.R
#takes in 8 parameters
#1 first lat point
#2 first lon point
#3 second lat point
#4 second lon point 
#5 start year
#6 end year
#7 what you want selected ex "ALL"
#8 the output folder
library(DaymetR)
args <- commandArgs(trailingOnly = TRUE)
result <- get.Daymet.tiles(lat1=as.numeric(args[1]),lon1=as.numeric(args[2]),lat2=as.numeric(args[3]),lon2=as.numeric(args[4]),start_yr=as.numeric(args[5]),end_yr=as.numeric(args[6]),param=args[7])
resultpath <- as.character(args[8])
write(result,file=paste(resultpath,'daymet_result',sep='/'))
