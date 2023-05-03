"""Definition of attribute OrderType"""
from uc3m_logistics.attributes.attribute import Attribute

class OrderType(Attribute):
    """Definition of attribute OrderType class"""

    # pylint: disable=super-init-not-called, too-few-public-methods
    def __init__(self, attr_value):
        """Definition of attribute OrderType init"""
        self._validation_pattern = r"(Regular|Premium)"
        self._error_message = "order_type is not valid"
        self._attr_value = self._validate(attr_value)
