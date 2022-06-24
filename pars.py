import json

mat=[]

with open("маты.txt", encoding="utf-8") as fi:
    for i in fi:
        mt = i.lower().strip().split("\n")[0]
        if mt != "":
            mat.append(mt)

with open("matt.json","w", encoding="utf-8")as f:
    json.dump(mat, f)