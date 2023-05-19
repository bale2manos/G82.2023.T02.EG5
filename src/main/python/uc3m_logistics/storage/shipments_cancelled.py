"""OrdersJsonStore definitoin"""
from uc3m_logistics.storage.json_store import JsonStore
from uc3m_logistics.cfg.order_manager_config import JSON_FILES_PATH
from uc3m_logistics.exception.order_management_exception import OrderManagementException

#pylint: disable=too-few-public-methods
class ShipmentsCancelled():
    """OrdersJsonStore singleton class"""
    #pylint: disable=invalid-name
    class __ShipmentsCancelled(JsonStore):
        """OrdersJsonStore private class"""
        _file_name = JSON_FILES_PATH + "shipments_cancelled.json"

        def add_item( self, item ):
            self.load_list_from_file()
            self._data_list.append(item)
            self.save_list_to_file()

    instance = None
    def __new__( cls ):
        if not ShipmentsCancelled.instance:
            ShipmentsCancelled.instance = ShipmentsCancelled.__ShipmentsCancelled()
        return ShipmentsCancelled.instance
    def __getattr__( self, nombre ):
        return getattr(self.instance, nombre)
    def __setattr__( self, nombre, valor ):
        return setattr(self.instance, nombre, valor)
