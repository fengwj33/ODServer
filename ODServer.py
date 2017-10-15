#!/usr/bin/python3
# -*- coding: utf-8 -*-
import web
import down
import pickle
import sys
import urllib
web.config.debug = False
urls = (
    "/","login",
    "/login", "login",
    "/logout", "logout",
    "/ctlpanel","ctlpanel",
    "/reset","reset"
)

file=open("pwd","rb+")
password=pickle.load(file)
file.close()


app= web.application(urls,globals())
render = web.template.render('templates/')
session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'login': False})
class login:
    def GET(self):
        if session.login:
            raise web.seeother('/ctlpanel')
        else:
            web.header('Content-Type','text/html;charset=UTF-8')
            return render.login("please input your password")
    def POST(self):
        print(web.input()["pwd"])
        if web.input()["pwd"]!=password:
            web.header('Content-Type','text/html;charset=UTF-8')
            return render.login("Password Error")
        else:
            session.login=True
            raise web.seeother('/ctlpanel')

class ctlpanel:
    def GET(self):
        if session.login:
            if web.input().__len__()!=0:
                print(web.input())
                if web.input()["cmd"]=="del":
                    down.removeFile(int(web.input()["id"]))
                elif web.input()["cmd"]=="get":
                    list=down.getFileList()
                    raise web.seeother( urllib.parse.quote('/static/'+list[0][int(web.input()["id"])]))
                raise web.seeother('/ctlpanel')
            else:
                list=down.getFileList()
                web.header('Content-Type','text/html;charset=UTF-8')
                return render.ctlpanel(str(list[0]),str(list[1]))
        else:
            raise web.seeother('/login')
    def POST(self):
        if web.input().__contains__("cmd"):
            if web.input()["cmd"]=="add":
                down.download(web.input()["url"],web.input()["file"])
            raise web.seeother('/ctlpanel')
        else:
            x = web.input(myfile={})
            filedir = sys.path[0]+"/static"
            if 'myfile' in x:
                filepath=x.myfile.filename.replace('\\','/') # replaces the windows-style slashes with linux ones.
                filename=filepath.split('/')[-1] # splits the and chooses the last part (the filename with extension)
                filename=filename.replace(" ","_")
                fout = open(filedir +'/'+ filename,'wb+') # creates the file where the uploaded file should be stored
                fout.write(x.myfile.file.read()) # writes the uploaded file to the newly created file.
                fout.close() # closes the file, upload complete.
            down.addLocal(filename)
            raise web.seeother('/ctlpanel')
            
        
class logout:
    def GET(self):
        session.login=False
        raise web.seeother('/login')
class reset:
    def GET(self):
        session.kill()
        web.header('Content-Type','text/html;charset=UTF-8')
        return "reset secccess"
    
if __name__== "__main__":
    app.run()
