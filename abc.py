'''
Author: Umesh
This prgroma meant ot achieve below
1
1+ 3 +1 
1 +3+ 5+ 3+ 1
1+ 3+ 5+ 7+ 5+ 3+ 1 
n


1:1
2:5
3:13
4:25

'''


n1=eval(input("Enter starting number: "))
n2=eval(input("Enter the ending number "))


# This is the outer loop to loop from and to numbers
for i in range(n1,n2+1): 
 c=0   # this is meant to make the counter 0 again 
 q=1
 j=1
 for j in range(1,i+1): 
  print(q)
  c=c+q
  q=q+2 # this is countign 1, 3, 5..
  #j=j+1 # this is counting 1,2,3..

 q=q-4 ## why do we hvae this?
 for j in range(1,i): 
  c=c+q
  print(q)
  q=q-2 # this is countign 3,1..

 print("Sum of the series for "+str(i) + " is " + str(c))




