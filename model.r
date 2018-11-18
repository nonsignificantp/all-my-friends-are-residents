library(lmtest)
library(Epi)

data = read_csv("./assets/data.csv")

model <- glm(mentions ~ offset(log(messanges)) + exposure + time, 
             family=quasipoisson,
             data=exposed_data)

summary(model)

round(ci.lin(model,Exp=T),3)

#             Estimate StdErr       z    P    expEst  2.5% 97.5%
# Intercept      0.425  0.022  19.233 0.00     1.530 1.465 1.598
# exposure      -1.926  0.176 -10.965 0.00     0.146 0.103 0.206
# time          -0.001  0.002  -0.332 0.74     0.999 0.995 1.003