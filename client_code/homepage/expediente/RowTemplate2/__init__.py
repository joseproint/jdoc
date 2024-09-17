from ._anvil_designer import RowTemplate2Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
from ...logo import Globals
import datetime
from datetime import datetime, timedelta
from datetime import date
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
    tTransOrigen=self.lbl_transaccion.text
    if tTransOrigen == 'TRANSFERENCIA' or tTransOrigen == 'DEVOLUCION':
      emailDestino = self.item['empRecibe']
      emailUsuario = Globals.f_getEmail()
      #alert(f"usuario:{emailUsuario} destino:{emailDestino}")
      if emailUsuario != emailDestino:
        alert('Solo el usuario destino puede acusar recibo del expediente!')
      else:
        numrecibo=self.link_nrecibo.text
        server_time = anvil.server.call('ServerTimeZone')
        fecha = server_time.strftime('%Y-%m-%d %H:%M:%S.%f')
        #codExpediente = Globals.f_getExpediente()
        codExpediente = expediente
        empRecibe = self.link_origen.text
        empEntrega = emailDestino
        notas = f"Acuse de Recibo del Expediente: {codExpediente}"
        tipotrans='ACUSERECIBO'
        numtrans = self.lbl_numero.text
        #esDevolucion = alert(f"Esta recibiendo la devolucion del documento {codExpediente}?",
        #         large=True,
        #         buttons=[("Si", True), ("No", False)])
        #if esDevolucion:
        #  alert('confirmado que es una devolución..')
        if numrecibo is None:
          #alert('Generando el Acuse de Recibo..')
          esDevolucion=False
          fRetorno=None #el acuse de recibo no guarda fecha de retorno
          #if anvil.server.call('transfiereExp',fecha,codExpediente,empRecibe,empEntrega,notas,tipotrans,numtrans,fRetorno,esDevolucion) is True:
          #  alert('Acuse de Recibo generado..')
        else:
          esDevolucion = alert(f"Esta devolviendo el documento {codExpediente}?",
                   large=True,
                   buttons=[("Si", True), ("No", False)])
          if esDevolucion:
            #alert('confirmado que es una devolucion..')
            alert(f"Devolucion confirmada de la Transferencia No.:{numtrans}")
            notas = f"Devolucion de la Transferencia No.{numtrans} y el Expediente: {codExpediente}"
          else:
            alert(f"Acuse Recibo confirmado No.:{numrecibo}")
            notas = f"Acuse de Recibo del Expediente: {codExpediente}"
          fRetorno=None #el acuse de recibo no guarda fecha de retorno
          tipotrans='DEVOLUCION'
        if anvil.server.call('transfiereExp',fecha,codExpediente,empRecibe,empEntrega,notas,tipotrans,numtrans,fRetorno,esDevolucion) is True:
          alert(f"{tipotrans} generado para una {tTransOrigen}..")

  def link_nrecibo_show(self, **event_args):
    """This method is called when the Link is shown on the screen"""
    if self.item['numrecibo'] is None:
      self.link_nrecibo.icon='fa:clock-o'
    else:
      self.link_nrecibo.icon='fa:handshake-o'

  def link_dias_show(self, **event_args):
    """This method is called when the Link is shown on the screen"""
    fRet=self.item['fRetorno']
    operacion=self.lbl_transaccion.text
    alert(f"operacion:{operacion} fRet={fRet}")
    if operacion=='TRANSFERENCIA':
      if fRet is not None:
        ano=fRet[:4]
        mes=fRet[6:2]
        dia=fRet[9:2]
        alert(f"ano:{ano} mes:{mes} dia:{dia}")
        fRetorno = datetime.datetime(ano,mes,dia)
        fHoy=datetime.today()
        y0 = fHoy.year
        m0 = fHoy.month
        d0 = fHoy.day
        #print(f"y0: {y0} m0: {m0} d0: {d0}")
        y1 = fRetorno.year
        m1 = fRetorno.month
        d1 = fRetorno.day
        #print(f"y1: {y1} m1: {m1} d1: {d1}")
        d0 = date(y0, m0, d0)
        d1 = date(y1, m1, d1)
        dias = d1 - d0
        #print(f"Dias: {dias.days}")
        diasfinal=dias.days
        #print(f"diasfinal: {diasfinal}")      
        self.link_dias.text=diasfinal
        if diasfinal<30:
          self.link_dias.foreground='green'
        elif diasfinal<60:
          self.link_dias.foreground='yellow'
        elif diasfinal<90:
          self.link_dias.foreground='orange'
        elif diasfinal<180:
          self.link_dias.foreground='red'
      else:
        self.link_dias.foreground='green'
