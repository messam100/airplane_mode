# Copyright (c) 2025, Mohammed Al-Qershi and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class FlightPassenger(Document):
	def before_save(self):
		parts = [self.first_name, self.last_name]
		self.full_name = " ".join(part for part in parts if part).strip()
