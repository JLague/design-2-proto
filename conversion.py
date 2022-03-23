# from base64 import encode
# from msilib.schema import Error
import numpy as np
from itertools import groupby
from operator import itemgetter
from pyzbar import pyzbar

forward={
    0:[3, 2, 1, 1],
    1:[2, 2, 2, 1],
    2:[2, 1, 2, 2],
    3:[1, 4, 1, 1],
    4:[1, 1, 3, 2],
    5:[1, 2, 3, 1],
    6:[1, 1, 1, 4],
    7:[1, 3, 1, 2],
    8:[1, 2, 1, 3],
    9:[3, 1, 1, 2],
}
reverse={
    0:[1, 1, 2, 3],
    1:[1, 2, 2, 2],
    2:[2, 2, 1, 2],
    3:[1, 1, 4, 1],
    4:[2, 3, 1, 1],
    5:[1, 3, 2, 1],
    6:[4, 1, 1, 1],
    7:[2, 1, 3, 1],
    8:[3, 1, 2, 1],
    9:[2, 1, 1, 3],
}

with open("data/barcode.txt") as data:
    array = np.loadtxt(data, delimiter=",")
code=array[:,0].astype(np.uint8)
temps=list(array[:,1])
#del code[:12]
#del code[-12:]
#del temps[:12]
#del temps[-12:]



def encode_list(s_list):
    RLE =[len(list(group))for key, group in groupby(s_list)]
    return RLE

def split(liste):
    for i in range(0, len(liste), 4):
        yield liste[i:i + 4]

x=list(split(encode_list(code)))
for i in range(0, len(x)):
    if len(x[i]) == 1:
        del x[i]
    if len(x[i]) == 2:
        del x[i]
    if len(x[i]) == 3:
        x[i].append(1)

def identification(liste):
    totdroite=[]
    totgauche=[]
    final=[]
    for i in range(0, len(x),1):
        l=x[i]
        rev=[]
        fev=[]
        for cle in forward:
            val=forward[cle]
            rev.append((cle,((l[0]-val[0])**2+(l[1]-val[1])**2+(l[2]-val[2])**2+(l[3]-val[3])**2)**0.5))
        totgauche.append(min(rev, key=itemgetter(1)))

        for cle in reverse:
            val=reverse[cle]
            fev.append((cle,((l[0]-val[0])**2+(l[1]-val[1])**2+(l[2]-val[2])**2+(l[3]-val[3])**2)**0.5))
        totdroite.append(min(fev, key=itemgetter(1)))
    #print(totgauche)
    #print(totdroite)
    for i,j in zip(totgauche, totdroite):
        if i[1]<j[1]:
            final.append((i[0]))
        else:
            final.append((j[0]))
    return(final)


print(code.tobytes())
print(pyzbar.decode((code.tobytes(), len(code), 1), symbols=[pyzbar.ZBarSymbol.UPCA]))
# print(identification(encode_list(code)))