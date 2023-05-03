"""Definition of attribute Email"""
from .attribute import Attribute

class Email(Attribute):
    """Definition of attribute email class"""

    # pylint: disable=super-init-not-called, too-few-public-methods
    def __init__(self, attr_value):
        """Definition of attribute email init method"""
        self._validation_pattern = r'^[a-z0-9]+([\._]?[a-z0-9]+)+[@](\w+[.])+\w{2,3}$'
        self._error_message = "contact email is not valid"
        self._attr_value = self._validate(attr_value)
