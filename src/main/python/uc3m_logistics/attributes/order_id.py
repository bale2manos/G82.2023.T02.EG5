"""Definition of attribute OrderId"""
from .attribute import Attribute

class OrderId(Attribute):
    """Definition of attribute OrderId class"""

    # pylint: disable=super-init-not-called, too-few-public-methods
    def __init__(self, attr_value):
        """Definition of attribute Orderid init"""
        self._validation_pattern = r"[0-9a-fA-F]{32}$"
        self._error_message = "order id is not valid"
        self._attr_value = self._validate(attr_value)
