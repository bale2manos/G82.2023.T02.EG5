"""Shipments storabe"""
from uc3m_logistics.storage.json_store import JsonStore
from uc3m_logistics.cfg.order_manager_config import JSON_FILES_PATH

#pylint: disable=invalid-name
class ShipmentsJsonStore():
    """ShipmentStore singleton class"""
    class __ShipmentsJsonStore(JsonStore):
        """ShipmnetsStore private class"""
        _file_name = JSON_FILES_PATH + "shipments_store.json"

    instance = None

    def __new__( cls ):
        if not ShipmentsJsonStore.instance:
            ShipmentsJsonStore.instance = ShipmentsJsonStore.__ShipmentsJsonStore()
        return ShipmentsJsonStore.instance

    def __getattr__( self, nombre ):
        return getattr(self.instance, nombre)

    def __setattr__( self, nombre, valor ):
        return setattr(self.instance, nombre, valor)
