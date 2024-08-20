from ._anvil_designer import logoTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
#import Push_Notifications
from anvil.tables import app_tables
from PasswordResetDialog import PasswordResetDialog
import Globals
from .. import hpGlobals
#from ..Estadisticas import estGlobals
from ..autor import autor

class logo(logoTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
      
    Globals.f_inicializa()
    hpGlobals.f_inicializa()
    #estGlobals.f_inicializa()
    
    # Any code you write here will run before the form opens.
    #try:
    #  from Push_Notifications import firebase
    #  PRINT('PASO 1')
    #except:
    #  print('You have not added Push Notifications dependency yet. Generate one by visiting https://push-notifications.anvil.app')
    #try:
    #  token=firebase.request_push_notifications()
    #  print('PASO 2')
    #  if firebase.not_exists(token): #Ensuring that the device is not already registered
    #    print('PASO 3')
    #    anvil.server.call('store_token',token) #Now we can store the token
    #    print('PASO 4')
    #except:
    #  Notification('Push Notifications are not supported on your browser. Please use a different browser',title='Registration Failed',style='danger').show()

  def button_login_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('homepage.login')
    #pdf = anvil.server.call('createPDF')
    #anvil.media.download(pdf)

  def form_show(self, **event_args):
    """This method is called when the column panel is shown on the screen"""
    #useremail = repr(anvil.get_url_hash()) #lee los parametros del URL despues del signo # para identificar el coach dueño del link en instagram
    useremail = anvil.get_url_hash() #lee los parametros del URL despues del signo # para identificar el coach dueño del link en instagram
    #anvil.alert(f"Our URL hash is: {useremail}")
    if useremail =="" or useremail=="''" or useremail is None:
      #anvil.alert("usermail empty")
      pass
    else:
      if isinstance(useremail, dict) and 'pwreset' in useremail:
        email=useremail['email']
        pwreset=useremail['pwreset']
        #anvil.alert(f"Paso 1: email:{email}, pwreset:{pwreset}")
        if not anvil.server.call('_is_password_key_correctSQL', email, pwreset):
          anvil.alert("This is not a valid password reset link")
          return
        while True:
          #anvil.alert('llegué aqui')
          pwr = PasswordResetDialog()
          if not anvil.alert(pwr, title="Reset Your Password", buttons=[("Reset password", True, 'primary'), ("Cancel", False)]):
            return
          if pwr.pw_box.text != pwr.pw_repeat_box.text:
            anvil.alert("Passwords did not match. Try again.")
          else:
            break
        if anvil.server.call('_perform_password_reset', email, pwreset, pwr.pw_box.text):
          #anvil.alert("Your password has been reset. You are now logged in.")
          anvil.alert("Your password has been reset. You can now Log in with new password.")
        else:
          anvil.alert("This is not a valid password reset link")          
      elif 'confirm' in useremail:
        #anvil.alert('paso 2')
        if anvil.server.call('_confirm_email_address', useremail['email'], useremail['confirm']):
          anvil.alert("Thanks for confirming your email address. You are now logged in.")
        else:
          anvil.alert("This confirmation link is not valid. Perhaps you have already confirmed your address?\n\nTry logging in normally.")
      elif 'email' in useremail:  
        #anvil.alert(f"useremail: {useremail}")
        #useremail = useremail[1:-1]
        useremail=useremail['email']
        if anvil.server.call('coachRegistrado',useremail):
          # usuario = anvil.server.call('fUsuario')
          # anvil.alert("El usuario es " + usuario)
          open_form('homepage.Registro',None,None, useremail)
        else:
          anvil.alert("Link is not valid, please ask your Coach about it!")
      else:
        anvil.alert(f"useremail: {useremail}")

  def link_pnotice_click(self, **event_args):
    """This method is called when the link is clicked"""
    #pass
    #anvil.server.call('f_setLastform',"logo")
    Globals.f_setLastform("homepage.logo")
    open_form('homepage.privacenotice')
    
  def link_tuse_click(self, **event_args):
    """This method is called when the link is clicked"""
    Globals.f_setLastform("homepage.logo")
    open_form('homepage.termsuse')

  def link_tservice_click(self, **event_args):
    """This method is called when the link is clicked"""
    Globals.f_setLastform("homepage.logo")
    open_form('homepage.termservice')

    








