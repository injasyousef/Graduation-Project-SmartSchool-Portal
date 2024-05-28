library(C50)
dataset=read.table(file="C:\\Users\\pc-2022\\OneDrive\\سطح المكتب\\DiabetesData.csv",header=T,sep=",")
df=as.data.frame(dataset)
df=df[order(runif(nrow(df))),]
training_set_size=floor(nrow(df)*0.7)
test_set_size=nrow(df)-training_set_size
training_set=df[1:training_set_size,]
test_set=df[test_set_size:training_set_size+test_set_size,]
M1=C5.0(training_set[,-9],training_set[,9]<- factor(training_set$Diabetic))
summary(M1)
predictions = predict(M1, newdata = test_set)
accuracy <- sum(predictions == test_set$Diabetic) / nrow(test_set)
accuracy=accuracy*100
accuracy
#-------------------------------------------------
training_set_size2=floor(nrow(df)*0.5)
test_set_size2=nrow(df)-training_set_size2
training_set2=df[1:training_set_size2,]
test_set2=df[(training_set_size2+1):nrow(df),]
M2=C5.0(training_set2[,-9],training_set2[,9]<- factor(training_set2$Diabetic))
summary(M2)
predictions2 = predict(M2, newdata = test_set2)
accuracy2 <- sum(predictions2 == test_set2$Diabetic) / nrow(test_set2)
accuracy2=accuracy2*100
accuracy2
#-------------------------------------------------
plot(M1,type="s")
plot(M2,type="s")
