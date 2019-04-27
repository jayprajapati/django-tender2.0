
def pkgen():
    import random	
    s="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    s=list(s)
    key=[]
    for i in range(15):
    	key.append(s[random.randint(0,len(s)-1)])
    key="".join(key)
		#pk=random.randint(100000000000,999999999999)
    return key

