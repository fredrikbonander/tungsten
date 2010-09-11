from DataFactory import dbUser
from gaesessions import get_current_session

from google.appengine.ext import db
import md5

def doLogin(username, password):
    user = dbUser.User.gql('WHERE username = :username', username = username).get()
        
    if user is None:
        return { 'status' : -1, 'message' : 'User doesn\'t exists' }
    
    m = md5.new()
    m.update(password)
    ## Passwords in dbUser is stored as MD5
    passwordAsMD5 = m.hexdigest()
    
    ## Match passed password as MD5 with dbUser password
    if user.password != passwordAsMD5:
        return { 'status' : -1, 'message' : 'Password missmatch' }
    
    session = get_current_session()
    session['user'] = { 'authenticated' : True, 'premissionLevel' : user.premissionLevel }
    # Let's try save a dict
    #session['user_premissionLevel'] = user.premissionLevel
    
    return { 'status' : 1, 'message' : 'User logged in' }

def doLogout():
    session = get_current_session()
    del session['user']
    #del session['user_premissionLevel']
    
    return { 'status' : 1, 'message' : 'User logged out' }

def isUserAuthenticated():
    session = get_current_session()
    if session and 'user' in session and session['user']['authenticated'] == True:
        return True
    else:
        return False
    
def AddOrUpdate(params):
    if not params.get('user_id'):
        user = dbUser.User()
        
    m = md5.new()
    m.update(params.get('password'))
    
    user.username = params.get('username')
    user.password = m.hexdigest()
    user.premissionLevel = params.get('premissionLevel')
    
    db.put(user)
    
    
    
    