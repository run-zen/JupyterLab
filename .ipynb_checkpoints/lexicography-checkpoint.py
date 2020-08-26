n=int(input())

org = input()
s= []
for e in org:
    s.append(e)

while(123-ord(max(s)) <=n):
    i= s.index(max(s))
    c = max(s)
    t = 123- ord(c)
    s[i] = chr( ord(c) - (26- t))
    n= n-t

l = len(s)-1
s[l] = chr(ord(s[l]) + n)
print(s)
        
        
