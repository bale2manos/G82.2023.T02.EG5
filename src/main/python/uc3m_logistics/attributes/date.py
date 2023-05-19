"""Definition of attribute TrackingCode"""
from uc3m_logistics.attributes.attribute import Attribute
from   datetime import datetime

# pylint: disable=too-few-public-methods
class Date(Attribute):
    """Definition of attribute Date class"""

    # pylint: disable=super-init-not-called
    def __init__(self, attr_value):
        """Definition of attribute TrackingCode init"""
        self._validation_pattern = r"\b\d{2}-\d{2}-\d{4}\b"
        self._error_message = "date format is not valid"
        self._attr_value = self._validate(attr_value)

    def _validate( self, attr_value ):
        """overrides validate method"""
        if not isinstance(attr_value, str):
            raise TypeError("date must be a string")
        super()._validate(attr_value)
        day = int(attr_value[0:2])
        month = int(attr_value[3:5])
        year = int(attr_value[6:10])
        if day < 1 or day > 31:
            raise ValueError("day is not valid")
        if month < 1 or month > 12:
            raise ValueError("month is not valid")
        if year < 1900 or year > 3000:
            raise ValueError("year is not valid")

        self.check_date_not_past(attr_value)
        return self._invert_date(attr_value)

    def check_date_not_past(self, attr_value):
        # Convertir la cadena a un objeto datetime
        fecha_datetime = datetime.strptime(attr_value, '%d-%m-%Y')
        # Obtener el timestamp de la fecha
        timestamp = fecha_datetime.timestamp()
        # Obtener la fecha actual
        fecha_actual = datetime.now()
        # Obtener el timestamp de la fecha actual
        timestamp_actual = fecha_actual.timestamp()
        # Comprobar que la fecha no sea anterior a la actual
        if timestamp < timestamp_actual:
            raise ValueError("date is not valid")

    @staticmethod
    def _invert_date(date):
        day = int(date[0:2])
        month = int(date[3:5])
        year = int(date[6:10])
        return str(year) + "-" + str(month) + "-" + str(day)