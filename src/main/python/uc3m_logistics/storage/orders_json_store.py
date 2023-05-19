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
        def remove_item(self, value, key):
            self.load_list_from_file()
            order_found = self.find_item(value, key)
            if not order_found:
                raise OrderManagementException("order_id not found")
            self._data_list.remove(order_found)
            self.save_list_to_file()
            return order_found

        def find_items_2_keys(self, value1, value2, key1, key2):
            items_found = []
            self.load_list_from_file()
            print(self._data_list)
            print(value1, value2, key1, key2)
            for item in self._data_list:
                if item[key1] == value1 and item[key2] == value2:
                    items_found.append(item)
            return items_found



    instance = None
    def __new__( cls ):
        if not OrdersJsonStore.instance:
            OrdersJsonStore.instance = OrdersJsonStore.__OrdersJsonStore()
        return OrdersJsonStore.instance
    def __getattr__( self, nombre ):
        return getattr(self.instance, nombre)
    def __setattr__( self, nombre, valor ):
        return setattr(self.instance, nombre, valor)
