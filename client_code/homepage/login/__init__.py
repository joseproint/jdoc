from ._anvil_designer import loginTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import datetime
from datetime import datetime, timedelta
from datetime import date
from ..logo import Globals

usuario=""

class login(loginTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    #open_form('homepage')
    email=self.text_box_email.text
    password=self.text_box_password.text
    hashedPass = anvil.server.call('hash_password2',password)
    anvil.server.call('fPruebaHash',email,password,hashedPass)

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    email = self.text_box_email.text
    password = self.text_box_password.text
    anvil.server.call('fComparaHash',email,password)

  def text_box_1_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    pass

  def link_login_click(self, **event_args):
    """This method is called when the link is clicked"""
    email=self.text_box_email.text
    password=self.text_box_password.text
    try:
      #respuestaOk=anvil.server.call('userOk',email,password)
      usuario=anvil.server.call('userOk',email,password)
      if usuario is None:
        respuestaOk=False
      else:
        respuestaOk=True        
      if respuestaOk:
        #usuario = anvil.server.call('fUsuario')
        #anvil.alert("El usuario es " + usuario)
        #print(f"El usuario es {usuario}")
        Globals.f_setEmail(email)
        #FuPago=anvil.server.call('fFuPago',email)
        role=anvil.server.call('roleEmpleado',email)
        #print(f"FuPago: {FuPago}")
        #self.deviceTokens(email) #valida si el dispositivo está registrado en la cuenta de jClockApp en la plataforma de notificación google firebase
        #if self.fCtaVencida(FuPago) and role!="Empleado":
        #  anvil.alert(f"Last payment date: {FuPago}. Please proceed with payment before continue!")
        #  open_form('homepage.pago')
        #else:
        #if role=="Empleado":
        #  open_form('homepage.mainmenu', usuario)
        open_form('homepage.mainmenu')
          #open_form('homepage.ponches')
        #else:
        #  open_form('homepage')
      else:
        anvil.alert("Invalid Email/Password!")
    except anvil.server.AppOfflineError:
      anvil.alert("You're disconnected from Internet or the Server is down, please try later...")

  def fCtaVencida(self,FuPago):
    fLimite=datetime.today() + timedelta(days=-31)
    if isinstance(FuPago,str):
        #datetime.strptime(FuPago, "%Y%m%d%H%M%S").date()
        y0=int(FuPago[:4])
        m0=int(FuPago[5:7])
        d0=int(FuPago[8:10])
        print(f"{FuPago} : {y0}-{m0}-{d0}")
    else:    
        y0 = FuPago.year
        m0 = FuPago.month
        d0 = FuPago.day
    #print(f"y0: {y0} m0: {m0} d0: {d0}")
    y1 = fLimite.year
    m1 = fLimite.month
    d1 = fLimite.day
    #print(f"y1: {y1} m1: {m1} d1: {d1}")
    d0 = date(y0, m0, d0)
    d1 = date(y1, m1, d1)
    dias = d1 - d0
    #print(f"Dias: {dias.days}")
    diasfinal=dias.days
    #print(f"diasfinal: {diasfinal}")
    if diasfinal>30:
      return True
    else:
      return False
    
  def link_signup_click(self, **event_args):
    """This method is called when the link is clicked"""
    #open_form('homepage.forgotPass')
    open_form('homepage.signup')

  def link_forgot_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('homepage.forgotPass')

  def link_home_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('homepage')

  def deviceTokens(self,uEmail):
    try:
      from Push_Notifications import firebase
    except:
      #print('You have not added Push Notifications dependency yet. Generate one by visiting https://push-notifications.anvil.app')
      print('Notifications are disable right now, we are working on it, sorry for the inconvenience!')
    try:
      token=firebase.request_push_notifications()
      if firebase.not_exists(token): #Ensuring that the device is not already registered
        #alert(f"email: {uEmail}")
        #alert(f"token: {token}")
        anvil.server.call('store_token',token,uEmail) #Now we can store the token
    except:
      #Notification('Push Notifications are not supported on your browser. Please use a different browser',title='Registration Failed',style='danger').show()
      Notification("Please add https://jClock.App to the home screen of your device, and accept notifications when asked for permissions. Thanks!",title='Registration Failed',style='danger').show()