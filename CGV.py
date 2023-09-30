def enc(x):
    out=""
    state=1
    for l in x:
        new=ord(l)
        if state==1: new+=5
        elif state==2: new+=8
        elif state==3: new+=3
        elif state==4: new+=6; state=0
        out+=chr(new)
        state+=1
    return out[::-1]

def dec(x):
    out=""
    state=1
    for l in x[::-1]:
        new=ord(l)
        if state==1: new-=5
        elif state==2: new-=8
        elif state==3: new-=3
        elif state==4: new-=6; state=0
        out+=chr(new)
        state+=1
    return out