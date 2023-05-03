"""Definition of attribute TrackingCode"""
from uc3m_logistics.attributes.attribute import Attribute

# pylint: disable=too-few-public-methods
class TrackingCode(Attribute):
    """Definition of attribute TrackingCode class"""

    # pylint: disable=super-init-not-called
    def __init__(self, attr_value):
        """Definition of attribute TrackingCode init"""
        self._validation_pattern = r"[0-9a-fA-F]{64}$"
        self._error_message = "tracking_code format is not valid"
        self._attr_value = self._validate(attr_value)
