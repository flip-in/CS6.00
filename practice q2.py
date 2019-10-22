x = '11010'
y=0
for i in range(len(x)):
    #print i
    #print 2**i
    y += int(x[i])*(2**i)
    print y
#print y
