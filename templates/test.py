def ascii_deletion_distance(str1, str2):
    myDict = {}
    myDict2 = {}
    
    for char in str1:
        myDict[char] = myDict.get(char,0) + 1
    for char in str2:
        if char in myDict:
            myDict[char] -= 1
        else:
            myDict2[char] = myDict.get(char,0) + 1
    
    for k,v in myDict2.items():
        if v > 0:
            myDict[k] = myDict.get(v,0) + 1
    
    tot = 0
    print myDict
    for k,v in myDict.items():
        if v > 0:
            tot += ord(k)*v
            
    return tot



ascii_deletion_distance("thought", "sloughs")