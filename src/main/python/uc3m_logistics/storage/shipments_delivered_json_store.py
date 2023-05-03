"""Shipments Delivered Store"""
from uc3m_logistics.storage.json_store import JsonStore
from uc3m_logistics.cfg.order_manager_config import JSON_FILES_PATH
#pylint: disable=too-few-public-methods
class ShipmentDeliveredJsonStore():
    """"Shipments Store singleton class"""
    #pylint: disable=invalid-name
    class __ShipmentDeliveredJsonStore(JsonStore):
        _file_name = JSON_FILES_PATH + "shipments_delivered.json"

    instance = None
    def __new__( cls ):
        if not ShipmentDeliveredJsonStore.instance:
            ShipmentDeliveredJsonStore.instance = \
                ShipmentDeliveredJsonStore.__ShipmentDeliveredJsonStore()
        return ShipmentDeliveredJsonStore.instance
    def __getattr__( self, nombre ):
        return getattr(self.instance, nombre)
    def __setattr__( self, nombre, valor ):
        return setattr(self.instance, nombre, valor)
