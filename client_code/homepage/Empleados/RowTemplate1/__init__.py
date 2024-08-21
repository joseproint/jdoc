from ._anvil_designer import RowTemplate1Template
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import stripe.checkout
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ...logo import Globals

class RowTemplate1(RowTemplate1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def label_nombre_show(self, **event_args):
    """This method is called when the Label is shown on the screen"""
    print(f"{self.label_nombre.text}")

  def link_editar_click(self, **event_args):
    """This method is called when the link is clicked"""
    print(f"self.item: {self.item}")
    open_form('homepage.Empleado',self.label_nombre.text, self.item )
    
  def link_borrar_click(self, **event_args):
    save_clicked = alert(f"Are you sure you want to delete {self.label_nombre.text}?",
                   large=True,
                   buttons=[("yes", True), ("Cancel", False)])
    if save_clicked:
      #anvil.server.call('deleteEmpFromGrid', self.item)
      empresa = Globals.f_getEmpresa()
      email = self.label_email.text
      anvil.server.call('delete_EmpleadoSql', email, empresa)
      anvil.server.call('delete_userSql',email,empresa)
      #anvil.server.call('delete_Cliente', self.text_box_email.text)
      #get_open_form().raise_event('x-refresh')
      self.parent.raise_event('x-refresh')

