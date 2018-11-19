library(lmtest)
library(sandwich)

# LOAD data.csv inside assets

model = glm('ratio ~ exposure + time + exposure:time',
            family=gaussian(link = 'identity'),
            data = data)

summary(model)

coeftest(model, vcov=vcovHAC)
sqrt(diag(vcovHAC(model))) # Standard errors

#                Estimate  Std. Error z value Pr(>|z|)      lowCI   upCI
# (Intercept)    0.0972698  0.0096298 10.1009  < 2e-16 ***
# exposure      -0.1845160  0.0826954 -2.2313  0.02566 *   -0.267 -0.101
# time          -0.0025860  0.0025194 -1.0264  0.30468    
# exposure:time  0.0143197  0.0077513  1.8474  0.06469 .