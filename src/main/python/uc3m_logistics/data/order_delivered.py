"""OrderDelivered Info"""
from datetime import datetime
from freezegun import freeze_time
from uc3m_logistics.attributes.tracking_code import TrackingCode

from uc3m_logistics.storage.shipments_delivered_json_store import ShipmentDeliveredJsonStore
from uc3m_logistics.inputs.deliver_input_file import DeliverInputFile


#pylint: disable=too-few-public-methods
class OrderDelivered():
    """OrderDelivered Class"""
    def __init__(self, tracking_code):
        self._tracking_code = TrackingCode(tracking_code).value
        self._delivery_day = str(datetime.today().date())


    def save( self ):
        """Saves the delivery info into the store"""
        orders_delivered_shipmens_store = ShipmentDeliveredJsonStore()
        orders_delivered_shipmens_store.add_item(self)

    def modify_date(self):
        """modifies the delivery info into the store"""
        orders_delivered_shipmens_store = ShipmentDeliveredJsonStore()
        orders_delivered_shipmens_store.modify_item(self)




    @classmethod
    def get_order_deliver_from_file( cls, input_file ):
        """gets the order from the store"""
        deliver_input_file = DeliverInputFile(input_file)
        my_new_deliver = cls(tracking_code=deliver_input_file.tracking_code)
        my_new_deliver._delivery_day = deliver_input_file.date
        return my_new_deliver


