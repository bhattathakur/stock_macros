#Calculates the fibonacci retracement level based on the Highest level of interest
#common ratios: 23.6%, 38.2%, 50%, 61.8%, and 78.6%.
levels=[23.6, 38.2, 50, 61.8,78.6]
high=float(input("Enter the highest value of interest: "))

fmt='{:5.1f}% level: {:>0.2f}'

print(fmt.format(100,high))

for i in levels[::-1]:
    print(fmt.format(i,high*i/100))
