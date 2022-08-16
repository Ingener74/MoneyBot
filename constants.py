# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from Purchase.PurchaseConfig import PurchaseConfig
from money.product import ProductConfig

CREDENTIAL_FILE = "creds.json"
purchase_config = PurchaseConfig("I", "K", "L", "N", "O", "J", 9)
products_config = ProductConfig("I", "K", "L", "N", "J", "O", 9)
