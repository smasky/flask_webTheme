import hashlib
str='111111'
a=hashlib.sha224(str)
print(a.digest())