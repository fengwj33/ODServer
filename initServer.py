#!/usr/bin/python3
import pickle
import sys
pwd=str(sys.argv[1])
file=open("pwd","wb")
pickle.dump(pwd,file)
file.close()
tasklist=[]
file=open("tasks","wb")
pickle.dump(tasklist,file)
file.close()
