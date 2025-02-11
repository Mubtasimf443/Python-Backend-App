# بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ  ﷺ
# InshaAllah, By his marcy I will Gain Success

from fastapi import FastAPI,Response,Cookie,Body,status
from fastapi.responses import HTMLResponse,RedirectResponse,JSONResponse,FileResponse
from fastapi.staticfiles import StaticFiles
from pymongo.mongo_client import MongoClient
import uvicorn;
import os
from dotenv import load_dotenv
from typing import Annotated
import jwt
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel
import random
from json import dumps as JSON_stringify
from datetime import datetime, timedelta, timezone
from threading import Timer





# variables
load_dotenv()
myDatabaseClient=MongoClient(os.getenv("TEST_DATABASE"))
myDatabase=myDatabaseClient['notes_app']
Users=myDatabase['Users']
Notes=myDatabase['Notes']
app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
JWT_KEY=os.getenv("JWT_KEY")



class SignUpData(BaseModel) :
 name : str  
 email : str 
 password : str 


class LoginData(BaseModel) :
 email : str 
 password : str 

class NoteData(BaseModel) :
  title : str
  description : str

class StaticFilesCache(StaticFiles):
    def __init__(self, *args, cachecontrol="no-cache", **kwargs):
        self.cachecontrol = cachecontrol
        super().__init__(*args, **kwargs)

    def file_response(self, *args, **kwargs) -> Response:
        resp: Response = super().file_response(*args, **kwargs)
        resp.headers.setdefault("Cache-Control", self.cachecontrol)
        return resp


app.mount('/static',StaticFilesCache(directory='public',cachecontrol='no-cache'), name='static')




@app.get('/')
async def name(app_auth : Annotated[str | None, Cookie()] = None):
# if (app_auth == None) : return RedirectResponse('/auth/login')
 return HTMLResponse(content=(open('views/notes.html').read()))


@app.get('/auth/{name}')
def authPage(name):
   return HTMLResponse(content=(open('views/auth.html').read()))

@app.post('/api/auth/sign-up') 
async def signup(user : SignUpData, res: Response ):
   try:
      name , email , password =user.name, user.email, user.password
      name = name.strip()
      email = email.strip()
      password = password.strip()
      if (len(name) < 8 or len(name) > 100 ) : return pError('name invalid')
      if (len(email) < 8 or len(email) > 100 ) : return pError('email invalid')
      if (len(password) < 6 or len(password) > 100 ) : return pError('password invalid')
      if Users.find_one({'email' :email}) != None :
        res.status_code =400
        return ({ "error": { 'message' : 'You already have Created Account' }})
      temporraryVerificationPin =random.randrange(100000 ,999999)
      newUser=Users.insert_one({ 'name':name , 'email':email , 'password': password, "temporraryVerificationPin":temporraryVerificationPin})
      cookie=jwt.encode(payload={'email':email} ,key=os.getenv('JWT_KEY') , algorithm="HS256")
      expires=datetime.now(timezone.utc) + timedelta(seconds=60)
      res.set_cookie(key='notes_app_verification',value=cookie,expires=expires)
      res.status_code=201
      async def deleteAfter60(email):
         user=Users.find_one({'email' :email}) 
         if (user == None) :return
         if user['isRegisters'] ==True : return
         else :
           print('User Deleted')
           Users.delete_one({'_id' : user['_id']})
         return
      timeout=Timer(60.00,deleteAfter60, (email) )
      timeout.start()
      return res
   except NameError as error:
     print(repr(error))
     print('SomeThing Went Wrong')
     res.status_code=500
     return res
   except TypeError as error:
     print(repr(error))
     print('SomeThing Went Wrong')
     res.status_code=500
     return res
   except :
     print('SomeThing Went Wrong')
     res.status_code=500
     return res
   


@app.post('/api/auth/login') 
def login(user : LoginData, res: Response):
   email , password =user.email.strip(), user.password.strip()
   if (len(email) < 8 or len(email) > 100 ) : return pError('email invalid')
   if (len(password) < 6 or len(password) > 100 ) : return pError('password invalid')
   dbUser= Users.find_one({'email': email})
   if dbUser == None :
     res.status_code=400
     return {'error' : { 'message' :'Please Create a account' }}
   if dbUser['password'] ==password : 
     res.status_code=200
     cookie =jwt.encode(payload={'_id' : dbUser['_id'] } , key=os.getenv('JWT_KEY') , algorithm="HS256")
     expires=datetime.now(timezone.utc) + timedelta(days=float(90))
     res.set_cookie(key='app_auth', value=cookie , expires=expires)
     return {'success':True}
   else :
     res.status_code=400
     return {'error' :{'message' : 'Password Are not same'}}

@app.post('/api/auth/opt-verification') 
async def opt_verificaition(pin=None,notes_app_verification : Annotated[str | None , Cookie()] =None,res:Response=Response):
  try:
    if pin == None or notes_app_verification == None :
      res.status_code=402
      return errorJson(data='Please Add pin || You have to Create account account again')
    pin = int(pin)
    decodedDict= jwt.decode(jwt=notes_app_verification, key=JWT_KEY , algorithms='HS256')
    if decodedDict['email'] == None :
      res.status_code=400
      return errorJson(data='You are not allowed spaming')
    userEmail =  decodedDict['email'] 
    dbUser= Users.find_one({'email': userEmail})
    if dbUser==None : 
      res.status_code==400
      return errorJson(data='Your Account was deleted before so create account again')
    if dbUser['temporraryVerificationPin']!=pin:
      res.status_code=400
      return errorJson('Please Give the correct Opt code')
    cookie =jwt.encode(payload={'_id' : dbUser['_id'] } , key=os.getenv('JWT_KEY') , algorithm="HS256")
    expires=datetime.now(timezone.utc) + timedelta(days=float(90))
    res.set_cookie(key='app_auth', value=cookie , expires=expires)
    res.status_code=200
    return res
  except InvalidTokenError:
    res.status_code=402
    return {'error' : 'jwt is not valid'}
  except :
    print('server error')
    res.status_code=500
    return errorJson('server error')

@app.get('/favicon.ico')
def favicon():
 return FileResponse(path='public/img/logo2.jpg',media_type='image/jpg')

@app.get('/api/notes')
async def getNotes():
 notes = Notes.find()
 return Notes


@app.delete('/api/notes?{id}')
async def delNotes(id, res:Response):
 Notes.find_one_and_delete({'_id':id})
 res.status_code=204
 return 


@app.post('/api/notes')
async def getNotes(note :NoteData, res:Response):
 Notes.insert({'title': note.title , 'description' :note.description})
 res.status_code=201
 return {'success':True}


if __name__ == "__main__":
   uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

def pError(error):
 item= {'success' :False , 'error':{'name':"p error",'message' :error }}
 return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST ,content=item)

def errorJson(data : str | dict , name:str | None =None):
  if type(data) == str and name != None:
    return {'error': {'message' : data ,'type' : name }}
  if type(data) == str :
    return {'error': {'message' : data}}
  elif type(data) == dict :
    return { 'error': data  }