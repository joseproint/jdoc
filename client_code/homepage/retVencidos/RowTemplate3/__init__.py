from ._anvil_designer import RowTemplate3Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import time
from datetime import datetime, timedelta
from datetime import date

class RowTemplate3(RowTemplate3Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def link_dias_show(self, **event_args):
    """This method is called when the Link is shown on the screen"""
    fRet=self.item['fRetorno']
    operacion=self.item['tipotrans']
    #alert(f"operacion:{operacion} fRet={fRet}")
    if operacion=='TRANSFERENCIA':
      #alert('comenzando...')
      if fRet is not None:
        #alert("aqui voy...")
        ano=fRet[:4]
        mes=fRet[5:7]
        dia=fRet[8:10]
        #alert(f"ano:{ano} mes:{mes} dia:{dia}")
        #fRetorno = datetime(ano,mes,dia)
        fRetorno=datetime.strptime(fRet[:19], '%Y-%m-%d %H:%M:%S')
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
        dias = d0 - d1
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

  def link_editar_click(self, **event_args):
    """This method is called when the link is clicked"""
    codExpediente = self.lbl_transaccion.text
    expRow = anvil.server.call(
      'get_unExpSql',
      codExpediente
    )
    print(f"expRow: {expRow}")
    open_form('homepage.expediente',codExpediente, expRow )

