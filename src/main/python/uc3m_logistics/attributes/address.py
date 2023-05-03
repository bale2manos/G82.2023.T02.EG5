"""Definition of attribute address"""
from uc3m_logistics.attributes.attribute import Attribute

class Address(Attribute):
    """Definition of address class"""
    #pylint: disable=super-init-not-called, too-few-public-methods
    def __init__(self, attr_value):
        """overrides init method"""
        self._validation_pattern = r"^(?=^.{20,100}$)(([a-zA-Z0-9]+\s)+[a-zA-Z0-9]+)$"
        self._error_message = "address is not valid"
        self._attr_value = self._validate(attr_value)
