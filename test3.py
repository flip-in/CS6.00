vs = 'hello'

def comp(s):
     res = 0
     for c1 in s:
          res += 2
          for c2 in s:
               res -= 1
     return res 

assert type(s) == str
assert comp(s) == -(len(s)**2) + 2*len(s)