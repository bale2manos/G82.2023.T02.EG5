"""OrdersJsonStore definitoin"""
from uc3m_logistics.storage.json_store import JsonStore
from uc3m_logistics.cfg.order_manager_config import JSON_FILES_PATH
from uc3m_logistics.exception.order_management_exception import OrderManagementException
import json

#pylint: disable=too-few-public-methods
class DateZipStore(JsonStore):
    """OrdersJsonStore singleton class"""
    _file_name = JSON_FILES_PATH + "/date_zipcode/"
    #pylint: disable=invalid-name
    def __init__(self, date, zip_code):
        self.create_file(date, zip_code)
        self._file_name = self._file_name+date+zip_code+".json"

    def create_file( self, date, zip_code):
        new_file = self._file_name+date+zip_code+".json"
        try:
            with open(new_file, "w", encoding="utf-8", newline="") as file:
                json.dump(self._data_list, file, indent=2)
        except FileNotFoundError:
            self._data_list = []
        except json.JSONDecodeError as ex:
            raise OrderManagementException("JSON Decode Error - Wrong JSON Format") from ex
            # append the delivery info

    def save(self):
        try:
            with open(self._file_name, "w", encoding="utf-8", newline="") as file:
                json.dump(self._data_list, file, indent=2)
        except FileNotFoundError as ex:
            raise OrderManagementException("Wrong file or file path") from ex