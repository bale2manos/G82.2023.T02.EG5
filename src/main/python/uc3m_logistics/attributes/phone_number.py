"""Definition of attribute PhoneNumber"""
from uc3m_logistics.attributes.attribute import Attribute

class PhoneNumber(Attribute):
    """Definition of attribute PhoneNumber"""

    # pylint: disable=super-init-not-called, too-few-public-methods
    def __init__(self, attr_value):
        """Definition of attribute PhoneNumber init"""
        self._validation_pattern = r"^(\+)[0-9]{11}"
        self._error_message = "phone number is not valid"
        self._attr_value = self._validate(attr_value)
