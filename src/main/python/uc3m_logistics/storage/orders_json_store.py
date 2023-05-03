"""OrdersJsonStore definitoin"""
from uc3m_logistics.storage.json_store import JsonStore
from uc3m_logistics.cfg.order_manager_config import JSON_FILES_PATH
from uc3m_logistics.exception.order_management_exception import OrderManagementException

#pylint: disable=too-few-public-methods
class OrdersJsonStore():
    """OrdersJsonStore singleton class"""
    #pylint: disable=invalid-name
    class __OrdersJsonStore(JsonStore):
        """OrdersJsonStore private class"""
        _file_name = JSON_FILES_PATH + "orders_store.json"

        def add_item( self, item ):
            order_found = self.find_item(item.order_id, "_OrderRequest__order_id")
            if order_found:
                raise OrderManagementException("order_id is already registered in orders_store")
            super().add_item(item)

    instance = None
    def __new__( cls ):
        if not OrdersJsonStore.instance:
            OrdersJsonStore.instance = OrdersJsonStore.__OrdersJsonStore()
        return OrdersJsonStore.instance
    def __getattr__( self, nombre ):
        return getattr(self.instance, nombre)
    def __setattr__( self, nombre, valor ):
        return setattr(self.instance, nombre, valor)
