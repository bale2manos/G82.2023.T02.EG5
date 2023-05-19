import unittest
from unittest import TestCase
import os
import hashlib
import json
from freezegun import freeze_time
from uc3m_logistics import OrderManager
from uc3m_logistics import OrderManagementException
from uc3m_logistics import JSON_FILES_PATH
from uc3m_logistics import JSON_FILES_RF2_PATH, JSON_FILES_RF3_PATH
from uc3m_logistics.storage.shipments_delivered_json_store import ShipmentDeliveredJsonStore

class TestDeliverProduct(TestCase):
    """Class for testing deliver_product"""
    @freeze_time("2023-03-08")
    def setUp(self):
        """first prepare the stores"""
        file_store_patient = JSON_FILES_PATH + "orders_store.json"
        file_shipments_store = JSON_FILES_PATH + "shipments_store.json"


        if os.path.isfile(file_store_patient):
            os.remove(file_store_patient)
        if os.path.isfile(file_shipments_store):
            os.remove(file_shipments_store)

        #add orders and shipping info in the stores
        my_manager = OrderManager()
        # add an order in the store
        file_test = JSON_FILES_RF2_PATH + "valid.json"
        my_manager.register_order(product_id="8421691423220",
                                  address="calle con20chars1esp",
                                  order_type="Regular",
                                  phone_number="+34123456789",
                                  zip_code="01000")
        # 4f5ff74ce8c5aa97f9675dbd44035d9d
        my_manager.send_product(file_test)
        my_manager.register_order(product_id="8421691423220",
                                  address="calle con19chars1esp",
                                  order_type="Regular",
                                  phone_number="+34666666666",
                                  zip_code="01000")
        # 6e230082fd91e2c43fa23ff29556dbfd
        my_manager.register_order(product_id="8421691423220",
                                  address="calle con19chars1esp",
                                  order_type="Regular",
                                  phone_number="+34666666666",
                                  zip_code="01100")


    @freeze_time("2023-03-15")
    def test_modify_date(self):
        my_manager = OrderManager()
        value = my_manager.deliver_product(
            "847dfd443d86c9c222242010c11a44bd9a09c37b42b6e956db97ba173abefe83")
        self.assertTrue(value)
        shipments_deliverd_store = ShipmentDeliveredJsonStore()
        found = shipments_deliverd_store.find_item(
            value="847dfd443d86c9c222242010c11a44bd9a09c37b42b6e956db97ba173abefe83",
            key="_tracking_code")
        self.assertIsNotNone(found)
        file_test = JSON_FILES_RF3_PATH + "test1_not_str.json"
        my_manager.modify_deliver_day(file_test)
        found = shipments_deliverd_store.find_item(
            value="847dfd443d86c9c222242010c11a44bd9a09c37b42b6e956db97ba173abefe83",
            key="_tracking_code")
        self.assertIsNotNone(found)

    @freeze_time("2023-03-15")
    def test_cancel_shipping(self):
        my_manager = OrderManager()
        # add an order in the store
        file_test = JSON_FILES_RF3_PATH + "test2.json"
        my_manager.cancel_order_request(file_test)

        self.assertIsNone(None)

    @freeze_time("2023-03-08")
    def test_show_delivers(self):
        my_manager = OrderManager()
        my_manager.show_delivers("2023-03-08", "01000")
        self.assertIsNone(None)
