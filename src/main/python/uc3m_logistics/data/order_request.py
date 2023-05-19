"""MODULE: order_request. Contains the order request class"""
import hashlib
import json
from datetime import datetime
from uc3m_logistics.exception.order_management_exception import OrderManagementException
from uc3m_logistics.attributes.order_type import OrderType
from uc3m_logistics.attributes.product_id import ProductId
from uc3m_logistics.attributes.address import Address
from uc3m_logistics.attributes.phone_number import PhoneNumber
from uc3m_logistics.attributes.zip_code import ZipCode
from uc3m_logistics.attributes.date import Date
from uc3m_logistics.storage.orders_json_store import OrdersJsonStore
from uc3m_logistics.storage.shipments_json_store import ShipmentsJsonStore
from uc3m_logistics.storage.shipments_cancelled import ShipmentsCancelled
from uc3m_logistics.storage.date_zip_store import DateZipStore
from freezegun import freeze_time
from uc3m_logistics.inputs.order_input import OrderInputFile

class OrderRequest:
    """Class representing the register of the order in the system"""
    #pylint: disable=too-many-arguments
    def __init__( self, product_id, order_type,
                  delivery_address, phone_number, zip_code ):
        self.__product_id = ProductId(product_id).value
        self.__delivery_address = Address(delivery_address).value
        self.__order_type = OrderType(order_type).value
        self.__phone_number = PhoneNumber(phone_number).value
        self.__zip_code = ZipCode(zip_code).value
        justnow = datetime.utcnow()
        self.__time_stamp = datetime.timestamp(justnow)
        self.__order_id =  hashlib.md5(self.__str__().encode()).hexdigest()

    @classmethod
    def get_order_by_order_id( cls, order_id ):
        """creates the order from the file"""
        orders_store = OrdersJsonStore()
        item = orders_store.find_item(order_id, "_OrderRequest__order_id")
        if not item:
            raise OrderManagementException("order_id not found")
        # retrieve the orders data
        proid = item["_OrderRequest__product_id"]
        address = item["_OrderRequest__delivery_address"]
        reg_type = item["_OrderRequest__order_type"]
        phone = item["_OrderRequest__phone_number"]
        order_timestamp = item["_OrderRequest__time_stamp"]
        zip_code = item["_OrderRequest__zip_code"]
        # set the time when the order was registered for checking the md5
        with freeze_time(datetime.fromtimestamp(order_timestamp).date()):
            order = cls(product_id=proid,
                                 delivery_address=address,
                                 order_type=reg_type,
                                 phone_number=phone,
                                 zip_code=zip_code)
        if order.order_id != order_id:
            raise OrderManagementException("Orders' data have been manipulated")
        return order

    @classmethod
    def get_order_request_from_file(cls, input_file):
        """gets the order from the store"""
        order_file = OrderInputFile(input_file)
        orders_store = OrdersJsonStore()
        found = orders_store.find_item(order_file.order_id, "_OrderRequest__order_id")
        if not found:
            raise OrderManagementException("order_id not found")
        return order_file.order_id

    @classmethod
    def cancel_request(cls, order_id: str):
        """cancels the order"""
        cls.check_if_sent(order_id)
        orders_store = OrdersJsonStore()
        item_removed = orders_store.remove_item(order_id, "_OrderRequest__order_id")
        cls.add_to_cancelled(item_removed)

    @classmethod
    def add_to_cancelled(cls, item_removed):
        orders_cancelled = ShipmentsCancelled()
        orders_cancelled.add_item(item_removed)

    @staticmethod
    def check_if_sent(order_id):
        shipment_store = ShipmentsJsonStore()
        found = shipment_store.find_item(order_id, "_OrderShipping__order_id")
        if found:
            raise OrderManagementException("Order has been sent")

    @classmethod
    def show_delivers(cls, date_p, zip_code_p):
        date, zip_code, timestamp = cls.validate_date_zip_code(date_p, zip_code_p)
        orders = cls.orders_date_zip_code(timestamp, zip_code)
        cls.store_orders_date_zip_code(date, orders, zip_code)
    @classmethod
    def store_orders_date_zip_code(cls,date, orders, zip_code):
        date_file = ''.join(date.split('-'))
        storage = DateZipStore(date_file, zip_code)
        storage._data_list = orders
        storage.save()

    @staticmethod
    def orders_date_zip_code(timestamp, zip_code):
        orders_store = OrdersJsonStore()
        key1 = "_OrderRequest__time_stamp"
        key2 = "_OrderRequest__zip_code"
        shipments = orders_store.find_items_2_keys(timestamp, zip_code, key1, key2)
        return shipments

    @staticmethod
    def validate_date_zip_code(date, zip_code):
        day = int(date[8:10])
        if day < 10:
            day = "0" + str(day)
        month = int(date[5:7])
        if month < 10:
            month = "0" + str(month)
        year = int(date[0:4])
        date = str(day) + "-" + str(month) + "-" + str(year)
        date = Date(date).value
        timestamp= datetime.strptime(date, '%Y-%m-%d').timestamp()

        print(zip_code)
        zip_code = ZipCode(zip_code).value
        return date, zip_code, timestamp


    def save( self ):
        """saves the order into the store"""
        orders_store = OrdersJsonStore()
        orders_store.add_item(self)

    def __str__(self):
        return "OrderRequest:" + json.dumps(self.__dict__)


    @property
    def delivery_address( self ):
        """Property representing the address where the product
        must be delivered"""
        return self.__delivery_address

    @delivery_address.setter
    def delivery_address( self, value ):
        self.__delivery_address = value

    @property
    def order_type( self ):
        """Property representing the type of order: REGULAR or PREMIUM"""
        return self.__order_type
    @order_type.setter
    def order_type( self, value ):
        self.__order_type = value

    @property
    def phone_number( self ):
        """Property representing the clients's phone number"""
        return self.__phone_number
    @phone_number.setter
    def phone_number( self, value ):
        self.__phone_number = value

    @property
    def product_id( self ):
        """Property representing the products  EAN13 code"""
        return self.__product_id
    @product_id.setter
    def product_id( self, value ):
        self.__product_id = value

    @property
    def time_stamp(self):
        """Read-only property that returns the timestamp of the request"""
        return self.__time_stamp

    @property
    def order_id( self ):
        """Returns the md5 signature"""
        return self.__order_id

    @property
    def zip_code( self ):
        """Returns the order's zip_code"""
        return self.__zip_code
