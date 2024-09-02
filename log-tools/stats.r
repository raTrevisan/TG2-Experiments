x<-1
exec<-1
total <- matrix(ncol = 3 ,nrow = 5)
exp <- c("1_node_batch1","queueless_8000q", "queueless_16i")
recieved <- matrix(ncol = 5 ,nrow = 5)

while(exec<=3){
  while(x<=5){
    y <- paste("logs_log-", x, sep='')
    dir <- paste('./experiments/',exp[exec],'/',x,'/',y,'/',sep='')
    
    v2xnc<- read.csv(paste(dir,"parsed_ncv2x.log",sep=''), header = FALSE)
    dab <- read.csv(paste(dir,"parsed_dab.log",sep=''), header = FALSE)
    das <- read.csv(paste(dir,"parsed_das.log",sep=''), header = FALSE)
    mc  <- read.csv(paste(dir,"parsed_mc.log",sep=''), header = FALSE)
    v2x <- read.csv(paste(dir,"parsed_v2x.log",sep=''), header = FALSE)
    
  
    recieved[4,x] <- ((60000 - length(v2xnc$V2))/600)
    recieved[2,x] <- ((60000 - length(dab$V2))/600)
    recieved[3,x] <- ((60000 - length(das$V2))/600)
    recieved[1,x] <- ((3000 - length(mc$V2))/30)
    recieved[5,x] <- ((60000 - length(v2x$V2))/600)
    
    x <- x + 1
  }

pdf(paste(exp[exec],"loss.pdf", sep= ''))
l <- c("Mission Critical","DaB","DaS","V2XNC","V2X")
tab <- recieved
colnames(tab) <- c ("# 1","# 2","# 3","# 4","# 5")

barplot(tab, main = paste(exp[exec], "Losses Overall"),col = c("lightblue","mistyrose","lightcyan","lavender","cornsilk"),
        beside = TRUE, ylim = c(0,30), ylab = "Losses %", xlab = "Iteration")
legend("topright", legend = l, 
       fill = c("lightblue","mistyrose","lightcyan","lavender","cornsilk"), box.lty = 0.5, cex = 1,
        )
dev.off()

  total[1,exec] <- (recieved[1,1] + recieved[1,2] + recieved[1,3] + recieved[1,4] + recieved[1,5])/5 
  total[2,exec] <- (recieved[2,1] + recieved[2,2] + recieved[2,3] + recieved[2,4] + recieved[2,5])/5 
  total[3,exec] <- (recieved[3,1] + recieved[3,2] + recieved[3,3] + recieved[3,4] + recieved[3,5])/5
  total[4,exec] <- (recieved[4,1] + recieved[4,2] + recieved[4,3] + recieved[4,4] + recieved[4,5])/5
  total[5,exec] <- (recieved[5,1] + recieved[5,2] + recieved[5,3] + recieved[5,4] + recieved[5,5])/5
exec <- exec + 1
x <- 1
}


labs <- c("Static 1 node", "8000Q","16I")
tab <- total
colnames(tab) <- labs
pdf("experiment_batch_1.pdf")
barplot(tab, main = paste("Average Losses"),col = c("lightblue","mistyrose","lightcyan","lavender","cornsilk"),
        beside = TRUE, 
      #  ylim = c(0,30), 
        ylab = "Losses %", 
        xlab = "Configuration")
legend("topright", legend = l, 
       fill = c("lightblue","mistyrose","lightcyan","lavender","cornsilk"), box.lty = 0.5, cex = 1,
)
dev.off()

