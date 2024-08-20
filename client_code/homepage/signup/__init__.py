from ._anvil_designer import signupTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..logo import Globals
from .. import hpGlobals

class signup(signupTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.text_box_username.text = Globals.f_getUsername()
    self.text_box_email.text = Globals.f_getEmail()
    self.text_box_password.text = Globals.f_getPassword()
    self.text_box_repeatpass.text = Globals.f_getPassword()
    # Any code you write here will run before the form opens.

  def button_signup_click(self, **event_args):
    """This method is called when the button is clicked"""
    email = self.text_box_email.text
    password = self.text_box_password.text
    repeatedPass = self.text_box_repeatpass.text
    username = self.text_box_username.text
    foto = self.image_foto.source
    if (email != "") and (password !="") and (repeatedPass !="") and (username !=""):
      if self.check_box_agree.checked:
        if anvil.server.call('userRegistrado',email) is False:
          if password==repeatedPass:
            fecha=hpGlobals.f_fechaHoraHoy()
            fecha=fecha.date()
            user_row = anvil.server.call('creaUsuario',username,email,password,foto,fecha)
            anvil.alert(f"User {user_row['userEmail']} created")
            self.enviarCorreo()
            open_form('homepage.login')
          else:
            anvil.alert('Password and repeated password do not match, please try again!')
        else:
          anvil.alert('User is registered, try to Log in!')
      else:
        anvil.alert('Please, accept Terms and Conditions to proceed with sign up!')
    else:
        anvil.alert('Field is blank!')

  def link_login_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('homepage.login')

  def file_loader_1_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    if file != None:
      self.image_foto.source=file
    else:
      anvil.alert('FileLoader is not working')

  def enviarCorreo(self):
    """This method is called when the link is clicked"""
    origen= "jClock App Administration"
    destino="support@jClock.app"
    usuario=self.text_box_username.text
    email=self.text_box_email.text
    titulo=f"New Coach signed up: {usuario}"
    notas=f""" Hi, we have a new jClock user, {usuario} already signed up, Please follow up payment details to confirm user access, his/her email: {email}, Thanks! """
    anvil.server.call('fEmail',origen,destino,titulo,notas)

  def link_back_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('homepage.login')

  def check_box_1_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    pass

  def link_terms_click(self, **event_args):
    """This method is called when the link is clicked"""
    Globals.f_setLastform("homepage.signup")
    username = self.text_box_username.text
    email = self.text_box_email.text
    password = self.text_box_password.text
    Globals.f_setSignupForm(username,email,password)
    open_form('homepage.termsuse')




    