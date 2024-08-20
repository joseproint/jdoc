from ._anvil_designer import forgotPassTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil.http import url_encode
#import bcrypt
#from random import SystemRandom
import random
from random import choice
#random = SystemRandom()
import sys

class forgotPass(forgotPassTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def button_send_click(self, **event_args):
    """This method is called when the button is clicked"""
    email=self.text_box_email.text
    respuestaOk=anvil.server.call('supervisor_registered',email)
    if respuestaOk:
      #user_rowID=anvil.server.call('fCoachRowId',email)
      #user_row=anvil.server.call('fUserRow',user_rowID)
      user_row=anvil.server.call('get_datosUsuarioSql',email)
      password=user_row['userPass']
      userName=user_row['userName']
      
      #user = app_tables.users.get(email=email)
      if not user_row['userConfirmed_email']:
        #anvil.alert("aqui ando")
        #if user_row['userLink_key'] is None:
        if user_row['userPassword_hash'] is None or user_row['userPassword_hash'] == "": 
          #anvil.alert("aqui ando 2")
          #user_row['userLink_key'] = mk_token()
          #anvil.server.call('fguardaUserLink', user_row, mk_token())
          #anvil.server.call('fguardaUserPasswordHash', user_row, mk_token())
          #anvil.email.send(to=email, subject="Confirm your email address", text=f""" Hi, Thanks for signing up for our service. To complete your sign-up, click here to confirm your email address: {anvil.server.get_app_origin('published')}#?email={url_encode(user['email'])}&confirm={url_encode(user['link_key'])} Thanks! """)
          pass
      #anvil.server.call('fguardaUserLink', user_row, mk_token())
      token=mk_token()
      print(f"email:{email} token:{token}")
      #anvil.server.call('fguardaUserLinkSql',email, mk_token())
      anvil.server.call('fguardaUserLinkSql',email, token)
      #userName = "Maria Santos"
      user_row=anvil.server.call('get_datosUsuarioSql',email) #para refrescar variable ser_row
      print(f"Line 55 ==> user_row:{user_row}")
      self.enviarCorreo(userName, user_row)
      #self.enviarCorreo(userName)
      anvil.alert("We sent an email with password reset instructions!")
      open_form('homepage.login')
    else:
      anvil.alert(f"Email {email} is not registered, please talk to your jClock Platform Administrator to sign up...")
      #open_form('homepage.signup')
      open_form('homepage.login')

  def enviarCorreo(self,userName,user_row):
  #def enviarCorreo(self,userName):
    """This method is called when the link is clicked"""
    print("hola...")
    origen= "jClock App Support"
    destino=self.text_box_email.text
    email=self.text_box_email.text
    titulo=f"Reset Your jClock App Password"
    #nombreServidor="http://owbswcpspi01.prdweb.web:8080/"
    #nombreServidor="http://spimobile:8080/"
    nombreServidor="localhost"
    ##notas=f""" Hi {userName}, You've asked to reset the password to your jClock App account. To update your password, click the link below:  {anvil.server.get_app_origin('published')}#?email={url_encode(email)}&confirm={url_encode(user_row['userLink_key'])} Thanks! """
    print(f"ok {email} userLink:{user_row['userLink_key']}")
    notas=f"""
      Hi {userName},
      
      Someone has requested a password reset for your account. If this wasn't you, just delete this email.
      If you do want to reset your password, click here:
      
        {nombreServidor}#?email={url_encode(email)}&pwreset={url_encode(user_row['userLink_key'])}    
 
      Thanks!
      """
    #notas="Probando..."
    #print(f"notas: {notas}")
    anvil.server.call('fEmail',origen,destino,titulo,notas)
    print(f"origen:{origen} destino:{destino} titulo:{titulo} notas:{notas}")
    #anvil.server.call('fEmail',origen,destino,titulo,notas)

  def link_home_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('homepage')


def mk_token():
  """Generate a random 14-character token"""
  return "".join([random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789") for i in range(14)])
