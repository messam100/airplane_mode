# Copyright (c) 2025, Mohammed Al-Qershi and contributors
# For license information, please see license.txt

import frappe
from datetime import datetime
from frappe.model.document import Document
from dateutil.relativedelta import relativedelta


class RentPayment(Document):
    def validate(self):
        if self.subscription_start_date and self.subscription_duration:
            start_date = datetime.strptime(self.subscription_start_date, "%Y-%m-%d").date()
            months = int(self.subscription_duration)
            new_expiry = start_date + relativedelta(months=months)
            self.subscription_expiry_date = new_expiry

    def on_submit(self):
        self.status = "Paid"
        self.update_shop_status_and_data()
        
    def on_cancel(self):
        self.status = "Cancelled"
        self.update_cancel()

    def update_shop_status_and_data(self):
        shop = frappe.get_doc("Shop", self.shop)
        shop.lease_status = "Occupied"
        shop.contract_expiry_date = self.subscription_expiry_date
        shop.rent_amount = self.amount_paid
        shop.tenant = self.tenant
        shop.save()
 
    def update_cancel(self):
        shop = frappe.get_doc("Shop", self.shop)
        shop.lease_status = "Available"
        shop.contract_expiry_date = None
        shop.rent_amount = 0
        shop.tenant = None
        shop.save()

@frappe.whitelist()
def default_rent(docname):
    doc = frappe.get_doc("Rent Payment", docname)
    settings = frappe.get_single("Shop Settings")
    if settings.default_rent:
        doc.amount_paid = settings.default_rent
        return settings.default_rent
    return None