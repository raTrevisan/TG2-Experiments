x<-1
exp <- "1000q_batch1"
service <-"ncv2x"
while(x<=5){
  y <- paste("logs_log-", x, sep='')

  dir <- paste('/experiment/',exp,'/',x,'/',y,'/',sep='')

  histogram <- read.csv(paste(dir,"hist_",service,".log",sep=''),header=F)
  histogram_timeout <- read.csv(paste(dir,"hist_timeout_",service,".log",sep=''),header=F)
  #pdf(paste("hist",exp, service, x, ".pdf",sep = ''))
  
  
  hist(histogram$V2, breaks = 5, col='green', border='white', xlim =c(0,0.5), xlab = "Time (s)", 
              main = (paste(exp, x , service)), ylim=c(0,5000))
  hist(histogram_timeout$V2, breaks = "fd", col='red', border='white', xlim =c(0,1), ylim=c(0,1000), 
              add = TRUE)  
  
 # dev.off()
  x<- x + 1
}

x<-1
exp <- c("16i_batch1","32i_batch1","64i_batch1","128i_batch1",
         "1000q_batch1","2000q_batch1","4000q_batch1","8000q_batch1")
service <-"mc"
while(x<=8) {
hist_global = read.csv(paste('./experiments/',exp[x], "/hist_", service, "_global.log", sep=''),header = F)
hist_global_timeout = read.csv(paste('./experiments/',exp[x], "/hist_timeout_", service, 
                                     "_global.log", sep=''), header = F)
pdf(paste("./hist_scale_down_",service,"/hist_",exp[x],"_global_", service, ".pdf",sep=''))

hist(hist_global_timeout$V2, col='red',breaks = 1800, border='red',xlab = "Time (s)",xlim = c(0,10), 
     ylim=c(0,15000), main = (paste(exp[x], service, "global")))
hist(hist_global$V2, col='green',breaks = 1 ,border='green',xlim = c(0,10),add = TRUE)  
dev.off()
x <- x + 1
}

