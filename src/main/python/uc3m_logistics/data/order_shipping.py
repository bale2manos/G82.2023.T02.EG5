"""Contains the class OrderShipping"""
from datetime import datetime
import hashlib
from freezegun import freeze_time
from uc3m_logistics.inputs.send_input_file import SendInputFile
from uc3m_logistics.data.order_request import OrderRequest
from uc3m_logistics.storage.shipments_json_store import ShipmentsJsonStore
from uc3m_logistics.exception.order_management_exception import OrderManagementException
from uc3m_logistics.data.order_delivered import OrderDelivered
from uc3m_logistics.attributes.tracking_code import TrackingCode
from uc3m_logistics.attributes.email import Email
from uc3m_logistics.attributes.order_id import OrderId
from uc3m_logistics.attributes.date import Date
from uc3m_logistics.attributes.zip_code import ZipCode

#pylint: disable=too-many-instance-attributes
class OrderShipping():
    """Class representing the shipping of an order"""

    def __init__(self,  order_id, delivery_email):
        self.__alg = "SHA-256"
        self.__type = "DS"
        self.__order_id = OrderId(order_id).value
        order = OrderRequest.get_order_by_order_id(self.__order_id)
        self.__product_id = order.product_id
        self.__order_type = order.order_type
        self.__delivery_email = Email(delivery_email).value
        justnow = datetime.utcnow()
        self.__issued_at = datetime.timestamp(justnow)
        if self.__order_type == "Regular":
            delivery_days = 7
        else:
            delivery_days = 1
        #timestamp is represneted in seconds.microseconds
        #__delivery_day must be expressed in senconds to be added to the timestap
        self.__delivery_day = self.__issued_at + (delivery_days * 24 * 60 * 60)
        self.__tracking_code = hashlib.sha256(self.__signature_string().encode()).hexdigest()

    def __signature_string( self ):
        """Composes the string to be used for generating the tracking_code"""
        return "{alg:" + self.__alg + ",typ:" + self.__type + ",order_id:" + \
               self.__order_id + ",issuedate:" + str(self.__issued_at) + \
               ",deliveryday:" + str(self.__delivery_day) + "}"

    @classmethod
    def get_order_shipping_from_file( cls, input_file ):
        """gets the order from the store"""
        send_input_file = SendInputFile(input_file)
        my_order_shipping = cls(order_id=send_input_file.order_id,
                                delivery_email=send_input_file.contact_email)
        return my_order_shipping

    @classmethod
    def get_order_shipping_from_tracking_code( cls, tracking_code ):
        """gets the shimpent from the store"""
        shipments_store = ShipmentsJsonStore()
        shipment_info = shipments_store.find_item(TrackingCode(tracking_code).value,
                                                  "_OrderShipping__tracking_code")
        if not shipment_info:
            raise OrderManagementException("tracking_code is not found")
        with freeze_time(datetime.fromtimestamp(shipment_info["_OrderShipping__issued_at"]).date()):
            shipment = cls(order_id=shipment_info["_OrderShipping__order_id"],
                           delivery_email=shipment_info["_OrderShipping__delivery_email"])
        return shipment

    def can_be_delivered( self ):
        """checks if the shipmnet can be delivdered"""
        today = datetime.today().date()
        can_be = False
        if datetime.fromtimestamp(self.__delivery_day).date() == today:
            can_be = True
        return can_be

    def deliver( self ):
        """stores the delivery information"""
        if self.can_be_delivered():
            order_delivered = OrderDelivered(self.__tracking_code)
            order_delivered.save()
        else:
            raise OrderManagementException("Today is not the delivery date")
        return True



    @property
    def product_id( self ):
        """Property that represents the product_id of the order"""
        return self.__product_id

    @product_id.setter
    def product_id( self, value ):
        self.__product_id = value

    @property
    def order_id( self ):
        """Property that represents the order_id"""
        return self.__order_id

    @order_id.setter
    def order_id( self, value ):
        self.__order_id = value

    @property
    def email( self ):
        """Property that represents the email of the client"""
        return self.__delivery_email

    @email.setter
    def email( self, value ):
        self.__delivery_email = value

    @property
    def tracking_code( self ):
        """returns the tracking code"""
        return self.__tracking_code

    @property
    def issued_at( self ):
        """Returns the issued at value"""
        return self.__issued_at

    @issued_at.setter
    def issued_at( self, value ):
        self.__issued_at = value

    @property
    def delivery_day( self ):
        """Returns the delivery day for the order"""
        return self.__delivery_day

    def save( self ):
        """saves the shipments in the store"""
        shipments_store = ShipmentsJsonStore()
        shipments_store.add_item(self)
