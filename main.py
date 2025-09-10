from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import os
import urllib.request
import urllib.parse

app = FastAPI()
app.description = "Test"
app.nd = '111'
app.mount('/static', StaticFiles(directory='static'), 'static')
SESSION = {}
SESSION['user'] = 'unknown'
tpl_path = 'templates'
remurl = 'http://91.240.208.99:8080/cgi-bin/test1.py'

def get_template(tpl):
    fullname = os.path.join(tpl_path,tpl)
    if os.path.isfile(fullname):
       return (200,open(fullname).read())
    else:
       return (404,f"Template {tpl} not found")


def remquery(url,param={}):
    if len(param) > 0:
      addpar = '?'+urllib.parse.urlencode(param)
    else:
      addpar = ''
    req = urllib.request.urlopen(remurl+addpar)
    res = req.read()
    return res
    pass

@app.get("/")
async def index():
    '''Главная страница
    '''
    return FileResponse("templates/index.html")


@app.get('/login')
async def login():
    return FileResponse('templates/login.html')

@app.post('/login')
async def do_login(username: str = Form(min_length=3),
   password: str = Form(min_length = 6, max_length=32)):
   SESSION['user'] = username if username=='alex' else 'unknown user'

   return {"username": username, "pass":password}

@app.get('/logout')
async def logout():
   SESSION['user'] = 'unknown'
   return RedirectResponse('/')
    

#@app.get('/static/css/{name}')
#async def mainpage(name):
#    fpath = os.path.join('static',name)
#    return FileResponse(fpath)


@app.get("/users/me")
async def read_user_me(test="***"):
    ''' Тееущий пользователь'''
    
    return {"user_id": "the current user","session_user": SESSION['user'],"qs":test}

@app.get("/users/{user_id}")
async def read_user(user_id: str):
    '''Пользователь по коду'''
    if user_id < '100':
      return {"user_id": user_id,"session_user": SESSION['user']}
    else:
      return {"Error_User": user_id}
    
@app.get("/check")
async def check_list(fdate='today',todate='today'):
    SESSION['fdate']=fdate
    SESSION['todate'] = todate
    return FileResponse("templates/check.html")

@app.get("/api/check")
async def check_list_json(fdate='today',todate='today'):
   return {"data":['point 1','point 2','point 3','point 4'],
           "msg":"Check list "+(SESSION['fdate'] if SESSION['fdate']==SESSION['todate'] else SESSION['fdate']+' to '+SESSION['todate']) }
