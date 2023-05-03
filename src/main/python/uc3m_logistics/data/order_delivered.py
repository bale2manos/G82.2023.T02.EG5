"""OrderDelivered Info"""
from datetime import datetime
from uc3m_logistics.attributes.tracking_code import TrackingCode
from uc3m_logistics.storage.shipments_delivered_json_store import ShipmentDeliveredJsonStore


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
