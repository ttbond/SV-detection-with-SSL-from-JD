import numpy as np
a=np.array([[1,2,3],[4,5,6],[7,8,9]])
print(a)
a=a[:,[1]]
print(a[0])
b=[0,1,0]
a=np.delete(a,np.where(np.array(b)==0))
print(a)