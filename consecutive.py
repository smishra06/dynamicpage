string="1AABBBCCCC1AA"
#string="A"
count=1
length=""
if len(string)>1:
    for i in range(1,len(string)):
       if string[i-1]==string[i]:
          count+=1
       else :
           length += string[i-1]+" occurs "+str(count)+", "
           count=1
    length += (string[i]+" occurs "+str(count))
else:
    i=0
    length += (string[i]+" occurs "+str(count))
print (length)