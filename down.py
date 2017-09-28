#!/usr/bin/python3
import os
import pickle
import sys
def getFileList():
    file=open("tasks","rb+")
    list=pickle.load(file)
    file.close()
    states=[]
    for n in list:
        if os.path.exists("static/"+n+".finish"):
            states.append("finish")
        else:
            states.append("downloading")
    return [list,states]
def removeFile(id):
    id=int(id)
    list=getFileList();
    if list[1][id]=="finish":
        os.remove("static/"+list[0][id]+".finish")
        os.remove("static/"+list[0][id])
        flist=list[0]
        del flist[id]
        file=open("tasks","wb")
        pickle.dump(flist,file)
        file.close()
        return True
    else:
        return False
def download(url,filename):
    file=open("tasks","rb+")
    list=pickle.load(file)
    file.close()
    list.append(filename)
    file=open("tasks","wb")
    pickle.dump(list,file)
    file.close()
    os.system("nohup ./download.sh \""+url+"\" \""+filename+"\" &")
    return True
def addLocal(filename):
    os.system("echo \"finish\" >>" +sys.path[0]+"/static/" + filename +".finish")
    file=open("tasks","rb+")
    list=pickle.load(file)
    file.close()
    list.append(filename)
    file=open("tasks","wb")
    pickle.dump(list,file)
    file.close()
    
