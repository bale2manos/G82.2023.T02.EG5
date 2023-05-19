"""Module """

from uc3m_logistics.data.order_request import OrderRequest
from uc3m_logistics.data.order_shipping import OrderShipping
from uc3m_logistics.data.order_delivered import OrderDelivered


class OrderManager:
    """OrderManager singleton class"""
    #pylint: disable=invalid-name
    class __OrderManager:
        """Order Manager private class"""
        def __init__( self ):
            pass

        # pylint: disable=too-many-arguments
        def register_order( self, product_id: str,
                            order_type: str,
                            address: str,
                            phone_number: str,
                            zip_code: str ) -> str:
            """Register the orders into the order's file"""

            my_order = OrderRequest(product_id,
                                    order_type,
                                    address,
                                    phone_number,
                                    zip_code)
            my_order.save()
            return my_order.order_id

        # pylint: disable=too-many-locals
        def send_product( self, input_file ):
            """Sends the order included in the input_file"""
            my_sign = OrderShipping.get_order_shipping_from_file(input_file)
            my_sign.save()
            return my_sign.tracking_code

        def deliver_product( self, tracking_code ):
            """Register the delivery of the product"""
            shipment = OrderShipping.get_order_shipping_from_tracking_code(tracking_code)
            return shipment.deliver()

        def modify_deliver_day(self, input_file):
            """Modify the delivery day of the product"""
            new_deliver = OrderDelivered.get_order_deliver_from_file(input_file)
            new_deliver.modify_date()
            return True


        def cancel_order_request(self, input_file):
            """Cancel the shipping of the product"""
            order_id = OrderRequest.get_order_request_from_file(input_file)
            OrderRequest.cancel_request(order_id)
            return True

        def show_delivers(self, date, zip_code):
            """Show the delivers of the day"""
            OrderRequest.show_delivers(date, zip_code)
            return True

    instance = None

    def __new__( cls ):
        if not OrderManager.instance:
            OrderManager.instance = OrderManager.__OrderManager()
        return OrderManager.instance

    def __getattr__( self, nombre ):
        return getattr(self.instance, nombre)

    def __setattr__( self, nombre, valor ):
        return setattr(self.instance, nombre, valor)
