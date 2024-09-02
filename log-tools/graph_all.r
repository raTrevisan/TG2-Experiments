x<-1
while(x<=5){
  y <- paste("logs_log-", x, sep='')
  exp <- "16i"
  dir <- paste(exp,'/',x,'/',y,'/',sep='')
  
  well<- read.csv(paste(dir,"parsed_well.log",sep=''), header = FALSE)
  dab <- read.csv(paste(dir,"parsed_dab.log",sep=''), header = FALSE)
  das <- read.csv(paste(dir,"parsed_das.log",sep=''), header = FALSE)
  mc  <- read.csv(paste(dir,"parsed_mc.log",sep=''), header = FALSE)
  v2x <- read.csv(paste(dir,"parsed_v2x.log",sep=''), header = FALSE)
  
  pdf(file = paste(exp,x,".pdf",sep=''))
  plot(well$V1,well$V2, type = "l", frame = TRUE,pch=17,
       col ="purple", xlab = "Time (s)", ylab = "Messages", 
       xlim = c(0,2500), ylim= c(0,5000000), main=paste("Scaling on",exp,x,sep=' ')
  )
  lines(dab$V1,dab$V2, pch = 20, col = "blue", type = "l", lty = 1)
  lines(das$V1,das$V2, pch = 20, col = "green", type = "l", lty = 1)
  lines(mc$V1,mc$V2, pch = 20, col = "red", type = "l", lty = 1)
  lines(v2x$V1,v2x$V2, pch = 20, col = "black", type = "l", lty = 1)

  legend("topleft", legend=c(
    "Well Data","Discrete Automation (Big)","Discrete Automation (Small)"
    ,"Mission Critical Data","V2X"
  ),
  col=c(   "purple","blue","green"
           ,"red","black"
  ), 
  lty = c( 1,1,1,1,1), 
  cex=0.8
  )
  
  dev.off()
  x<- x + 1
}

