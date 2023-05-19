"""Send input file definition"""
import json
from uc3m_logistics.exception.order_management_exception import OrderManagementException
from uc3m_logistics.attributes.tracking_code import TrackingCode
from uc3m_logistics.attributes.date import Date


class DeliverInputFile():
    """send input file class"""
    def __init__(self, input_file):
        data = self.get_data_from_input_file(input_file)
        self.tracking_code = TrackingCode(data["tracking_code"]).value
        self.date = Date(data["date"]).value

    def get_data_from_input_file(self, input_file):
        """gets the data from the file"""
        try:
            with open(input_file, "r", encoding="utf-8", newline="") as file:
                data = json.load(file)
        except FileNotFoundError as ex:
            # file is not found
            raise OrderManagementException("File is not found") from ex
        except json.JSONDecodeError as ex:
            raise OrderManagementException("JSON Decode Error - Wrong JSON Format") from ex
        self.validate_inut_file_labels(data)
        return data

    def validate_inut_file_labels(self, data):
        """validates the labels"""
        if not "tracking_code" in data.keys():
            raise OrderManagementException("Bad label")
        if not "date" in data.keys():
            raise OrderManagementException("Bad label")
