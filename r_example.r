n <- 50
counter <- 1
a <- 0
b <- 1
temp <- 0

while (counter != n) {

    temp <- a + b
    a <- b
    b <- temp

    counter <- counter + 1
}