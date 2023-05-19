"""Shipments Delivered Store"""
from uc3m_logistics.storage.json_store import JsonStore
from uc3m_logistics.cfg.order_manager_config import JSON_FILES_PATH
from uc3m_logistics.exception.order_management_exception import OrderManagementException
from datetime import datetime
#pylint: disable=too-few-public-methods
class ShipmentDeliveredJsonStore():
    """"Shipments Store singleton class"""
    #pylint: disable=invalid-name
    class __ShipmentDeliveredJsonStore(JsonStore):
        _file_name = JSON_FILES_PATH + "shipments_delivered.json"


        def modify_item(self, item):
            self.load_list_from_file()


            for deliver in self._data_list:
                if deliver["_tracking_code"] == item._tracking_code:
                    old_date = deliver["_delivery_day"]
                    new_date = item._delivery_day
                    self.check_date(old_date, new_date)

                    deliver["_delivery_day"] = new_date
                    self.save_list_to_file()
                    return
            raise OrderManagementException("tracking code not found")


        @staticmethod
        def check_date(old_date, new_date):
            old_timestamp = datetime.strptime(old_date, '%Y-%m-%d')
            new_timestamp = datetime.strptime(new_date, '%Y-%m-%d')
            if old_timestamp > new_timestamp:
                raise OrderManagementException("new date is before old date")



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
