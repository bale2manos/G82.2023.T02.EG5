"""Send input file definition"""
import json
from uc3m_logistics.exception.order_management_exception import OrderManagementException
from uc3m_logistics.attributes.order_id import OrderId
from uc3m_logistics.attributes.email import Email


class SendInputFile():
    """send input file class"""
    def __init__(self, input_file):
        data = self.get_data_from_input_file(input_file)
        self.order_id = OrderId(data["OrderID"]).value
        self.contact_email = Email(data["ContactEmail"]).value

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
        if not "OrderID" in data.keys():
            raise OrderManagementException("Bad label")
        if not "ContactEmail" in data.keys():
            raise OrderManagementException("Bad label")
