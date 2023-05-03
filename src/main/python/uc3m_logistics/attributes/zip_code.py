"""Definition of attribute ZipCde"""
from uc3m_logistics.attributes.attribute import Attribute
from uc3m_logistics.exception.order_management_exception import OrderManagementException

class ZipCode(Attribute):
    """Definition of attribute ZipCode class"""

    # pylint: disable=super-init-not-called, too-few-public-methods
    def __init__(self, attr_value):
        """Definition of attribute ZipCode init"""
        self._attr_value = self._validate(attr_value)

    def _validate(self, attr_value):
        """Definition of attribute ZipCocd validation"""
        if attr_value.isnumeric() and len(attr_value) == 5:
            if (int(attr_value) > 52999 or int(attr_value) < 1000):
                raise OrderManagementException("zip_code is not valid")
        else:
            raise OrderManagementException("zip_code format is not valid")
        return attr_value
