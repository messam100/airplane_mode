# Copyright (c) 2025, Mohammed Al-Qershi and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class Tenant(Document):
	def after_insert(self):
		self.create_contact()
		self.create_address()

	def create_contact(self):
		existing_contact = frappe.get_all("Contact", filters={
            "first_name": self.tenant_name
        }, pluck="name")

		if existing_contact:
			frappe.msgprint(_("Contact already exists for this Tenant."))
			return

		contact = frappe.new_doc("Contact")

		contact.first_name = self.tenant_name
		contact.append("email_ids", {
            "email_id": self.email,
            "is_primary": 1
        })
		contact.append("phone_nos", {
            "phone": self.phone_number,
            "is_primary_phone": 1
        })
		contact.append("links", {
			"link_doctype": "Tenant",
			"link_name": self.name,
			"link_title": self.tenant_name
    	})

		contact.insert(ignore_permissions=True)

	def create_address(self):
		existing_address = frappe.get_all("Address", filters={
        	"address_title": self.tenant_name,
        	"address_type": "Billing"
    	}, pluck="name")

		if existing_address:
			frappe.msgprint(_("Address already exists for this Tenant."))
			return
    
		address = frappe.new_doc("Address")
		address.address_title = self.tenant_name
		address.address_line1 = self.address
		address.city = self.city
		address.country = self.country

		address.append("links", {
	        "link_doctype": "Tenant",
	        "link_name": self.name,
	        "link_title": self.tenant_name
	    })

		address.insert(ignore_permissions=True)
