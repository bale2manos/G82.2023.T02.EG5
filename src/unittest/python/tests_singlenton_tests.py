from unittest import TestCase
from uc3m_logistics import OrderManager
from uc3m_logistics.storage.shipments_json_store import ShipmentsJsonStore

class TestSingleton(TestCase):
    def test_singleton_order_manager( self ):
        om1 = OrderManager()
        om2 = OrderManager()
        om3 = OrderManager()

        self.assertEqual(om1,om2)
        self.assertEqual(om2,om3)
        self.assertEqual(om1,om3)

    def test_singlenton_shipments_json_store( self ):
        store1 = ShipmentsJsonStore()
        store2 = ShipmentsJsonStore()
        store3 = ShipmentsJsonStore()
        self.assertEqual(store1,store2)
        self.assertEqual(store2,store3)
        self.assertEqual(store1, store3)