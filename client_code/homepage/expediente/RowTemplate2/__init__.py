from ._anvil_designer import RowTemplate2Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
from ...logo import Globals
global expediente

class RowTemplate2(RowTemplate2Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    global expediente
    expediente = Globals.f_getExpediente()
    # Any code you write here will run before the form opens.

  def link_notas_click(self, **event_args):
    """This method is called when the link is clicked"""
    alert(f"Nota: {self.item['notas']}")

  def link_origen_click(self, **event_args):
    """This method is called when the link is clicked"""
    emailOrigen=self.item['empEntrega']
    #telefono = self.item['empTelefono']
    #telefono = f"({telefono[:3]}) {telefono[4:6]}-{telefono[7:]}"
    contacto=anvil.server.call('f_contactoEmpleado',emailOrigen)
    alert(f"Usuario Entrega:{contacto}")

  def link_destino_click(self, **event_args):
    """This method is called when the link is clicked"""
    emailDestino=self.item['empRecibe']
    contacto=anvil.server.call('f_contactoEmpleado',emailDestino)
    alert(f"Usuario Entrega:{contacto}")

  def link_nrecibo_click(self, **event_args):
    """This method is called when the link is clicked"""
    global expediente
    emailDestino = self.item['empRecibe']
    emailUsuario = Globals.f_getEmail()
    #alert(f"usuario:{emailUsuario} destino:{emailDestino}")
    if emailUsuario != emailDestino:
      alert('Solo el usuario destino puede acusar recibo del expediente!')
    else:
      numrecibo=self.link_nrecibo.text
      if numrecibo is None:
        alert('Generando el Acuse de Recibo..')
        server_time = anvil.server.call('ServerTimeZone')
        fecha = server_time.strftime('%Y-%m-%d %H:%M:%S.%f')
        #codExpediente = Globals.f_getExpediente()
        codExpediente = expediente
        empRecibe = self.link_origen.text
        empEntrega = emailDestino
        notas = f"Acuse de Recibo del Expediente: {codExpediente}"
        tipotrans='ACUSERECIBO'
        numtrans = self.lbl_numero.text
        if anvil.server.call('transfiereExp',fecha,codExpediente,empRecibe,empEntrega,notas,tipotrans,numtrans) is True:
          alert('Acuse de Recibo generado..')
      else:
        alert('Acuse Recibo No.:')
