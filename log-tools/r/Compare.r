cam <- read.csv("baseline_well/parsed_well.log", header = FALSE)
dab <- read.csv("baseline_well/parsed_dab.log", header = FALSE)
das <- read.csv("baseline_well/parsed_das.log", header = FALSE)
mc  <- read.csv("baseline_well/parsed_mc.log", header = FALSE)
v2x <- read.csv("baseline_well/parsed_v2x.log", header = FALSE)
#man <- read.csv("manager.csv", header = FALSE)

 # Give the chart file a name.
 pdf(file = "baseline_well_line.pdf")

 # Create a first line
 plot(cam$V1,cam$V2, type = "l", frame = TRUE,pch=17,
      col ="purple", xlab = "Tempo (s)", ylab = "Mensagens", xlim = c(0,3000), ylim= c(0,1000000), main= "Baseline w/ Well"
      )
 #Add a second line
 lines(dab$V1,dab$V2, pch = 20, col = "blue", type = "l", lty = 1)
 # Add a third line to the plot
 lines(das$V1,das$V2, pch = 20, col = "green", type = "l", lty = 1)
 # Add a fourth line to the plot
 lines(mc$V1,mc$V2, pch = 20, col = "red", type = "l", lty = 1)
 # Add a fifth line to the plot
 lines(v2x$V1,v2x$V2, pch = 20, col = "black", type = "l", lty = 1)
 
 par(new=TRUE)
 
 #plot(man$V1, man$V2, pch=15,  xlab="", ylab="", ylim=c(0,8), lty = 5,
 #     axes=FALSE, type="s", col="gold4")
# axis(4, ylim=c(0,8), col="gold4",col.axis="gold4",las=1)
 
 
#  Add a legend to the plot
 legend("topleft", legend=c(
        "Well Data"
       ,"Discrete Automation (Big)"
       ,"Discrete Automation (Small)"
       ,"Mission Critical Data"
       ,"V2X"
#       ,"Cluster Size"
),
col=c(   "purple"
        ,"blue"
        ,"green"
        ,"red"
        ,"black"
#        ,"gold4"
              ), 

lty = c( 1,1,1,1,1,5), 
cex=0.8

)


 dev.off() 
 
 