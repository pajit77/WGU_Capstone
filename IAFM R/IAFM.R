args <- commandArgs(trailingOnly = TRUE)

library(lme4)

preprocess <- function(origRollup, kcm) {
  #kcm_index <- grep(kcm,names(origRollup))
  kcm_index <- which(names(origRollup)==kcm)
  df <- origRollup[,c(3,5,7,15,kcm_index,kcm_index+1)]  # subset only the columns of interest
  df$First.Attempt <- gsub("incorrect", 0, df$First.Attempt)  # convert correctness coding to binary, numeric
  df$First.Attempt <- gsub("hint", 0, df$First.Attempt)
  df$First.Attempt <- gsub("correct", 1, df$First.Attempt)
  names(df) <- c("Anon.Student.Id","Problem.Name","Step.Name","Success","KC","Opportunity")  ## rename columns
  df$Success <- as.numeric(as.vector(df$Success))  # convert success and opportunity columns to numeric
  df$Opportunity <- as.numeric(as.vector(df$Opportunity)) - 1  # start opportunity count at 0
  return(df)
}

workingDir = "."



## preprocess data -- customize the file path & kc model with workflow inputs
df <- preprocess(data.frame(read.table(file="C:/Users/Pankaj/Documents/IAFMCode/SampleData.txt",na.string="NA",sep="\t",quote="",header=T)),
                 make.names("KC (Default)"))  ## make.names changes the inputted string to the same periods-based format that data.frame() does for column headers

## Here KC (Default) should be replaced by "Topic" or level at which data is collected for student performance. KC would be ideal. But topic is the best we can get at scale.


## fit iAFM - four params - student intercept, student slope, KC intercept, and KC slope
iafm.model <- suppressWarnings(glmer(Success ~ Opportunity + (Opportunity|Anon.Student.Id) + (Opportunity|KC), data=df, family=binomial()))

outputFile1 <- paste(workingDir, "/model-values.txt", sep="")

## potential outputs
write(paste("AIC",AIC(iafm.model),sep="\t"),file=outputFile1,sep="",append=FALSE)
write(paste("BIC",BIC(iafm.model),sep="\t"),file=outputFile1,sep="",append=TRUE)
write(paste("Log Likelihood",as.numeric(logLik(iafm.model)),sep="\t"),file=outputFile1,sep="",append=TRUE)
write(paste("MAIN EFFECT intercept",fixef(iafm.model)[[1]],sep="\t"),file=outputFile1,sep="",append=TRUE)
write(paste("MAIN EFFECT slope",fixef(iafm.model)[[2]],sep="\t"),file=outputFile1,sep="",append=TRUE)
outputFile2 <- paste(workingDir, "/parameters.txt", sep="")

# stud.params is a table where column 1 is the student ID, column 2 is the iAFM estimated student intercept, and column 3 is the iAFM estimated student slope
stud.params <- data.frame( cbind(row.names(ranef(iafm.model)$Anon.Student.Id), ranef(iafm.model)$Anon.Student.Id[,1], ranef(iafm.model)$Anon.Student.Id[,2]) )
stud.params <- cbind(Type="Student", stud.params)
colnames(stud.params) <- c("Type", "Name", "Intercept", "Slope")
write.table(stud.params,file=outputFile2,sep="\t",quote=FALSE,na="",col.names=TRUE,append=FALSE,row.names=FALSE)

# kc.params is a table where column 1 is the KC name, column 2 is the iAFM estimated KC intercept, and column 3 is the iAFM estimated KC slope
kc.params <- data.frame( cbind(row.names(ranef(iafm.model)$KC), ranef(iafm.model)$KC[,1], ranef(iafm.model)$KC[,2]) )
kc.params <- cbind(Type="Skill", kc.params)
write.table(kc.params,file=outputFile2,sep="\t",quote=FALSE,na="",col.names=FALSE,append=TRUE,row.names=FALSE)
