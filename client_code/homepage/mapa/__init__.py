from ._anvil_designer import mapaTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files


class mapa(mapaTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    rowCbienes = anvil.server.call('get_ClasesBienesSql')
    rowEstado = anvil.server.call('get_estadosBien')
    self.dd_clasesBienes.items = [(r['descripcion'], r['id'].strip()) for r in rowCbienes]
    self.dd_estado.items = [r for r in rowEstado]
    # Any code you write here will run before the form opens.

  def link_back_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('homepage.mainmenu')

  def button_buscar_click(self, **event_args):
    """This method is called when the button is clicked"""
    #dato = self.text_box_1.text
    clase = self.dd_clasesBienes.selected_value
    estado = self.dd_estado.selected_value
    if clase!='' and clase is not None and estado!='' and estado is not None:
      #datoOk=dato.replace(' ','%')
      rowAf=anvil.server.call('get_ExpedientesAll', clase, estado)
      if rowAf is not None:
        jsonObj=json.loads(rowAf)
        self.repeating_panel_1.items=jsonObj
        self.ploteaAf(jsonObj)
    else:
      Notification("pls type what you're looking for...").show()

  def ploteaAf(self,datos):
    #for row in self.repeating_panel_1.items:
    urlRedIcon="_/theme/redmarker.png"
    urlYellowIcon="_/theme/yellowmarker.png"
    for row in datos:
      lat=row['lat']
      lng=row['lng']
      notas=f"ID:{row['id']}-{row['descripcion']} in {row['nombredep']}"
      #print(notas)
      self.marcador(lat,lng,urlYellowIcon,notas)
      #self.map_1.center = GoogleMap.LatLng(lat,lng)
      #self.map_1.zoom = 8
      #marker = GoogleMap.Marker(
      #  animation=GoogleMap.Animation.DROP,
      #  position=GoogleMap.LatLng(lat,lng)
      #)
      #self.map_1.add_component(marker)

  def marcador(self,lat,lng,icono,notas):
    self.map_1.center = GoogleMap.LatLng(lat,lng)
    self.map_1.zoom = 8
    iconObj = GoogleMap.Icon(
      url=icono,
      scaled_size=GoogleMap.Size(40,40)
    )
    marker = GoogleMap.Marker(
      animation=GoogleMap.Animation.DROP,
      position=GoogleMap.LatLng(lat,lng),
      icon=iconObj
    )
    marker.tag =notas
    marker.add_event_handler("click", self.marker_click)
    self.map_1.add_component(marker)

  def marker_click(self, sender, **event_args):
    i =GoogleMap.InfoWindow(content=Label(text=sender.tag))
    i.open(self.map_1, sender)
    Globals.f_setLabel1(sender.tag)
    new_picture = {}
    # Open an alert displaying the 'ArticleEdit' Form
    save_clicked = alert(
      content=markertaginfo(item=new_picture),
      title="",
      large=False
      #buttons=[("Save", True), ("Cancel", False)],
    )
    # If the alert returned 'True', the save button was clicked.
    #if save_clicked:
    #  print("saved..")
    #else:
    #  print("canceled..")

