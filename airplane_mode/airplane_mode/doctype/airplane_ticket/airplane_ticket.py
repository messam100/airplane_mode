# Copyright (c) 2025, Mohammed Al-Qershi and contributors
# For license information, please see license.txt

import frappe
import random
from frappe import _
from frappe.model.document import Document


class AirplaneTicket(Document):
	def validate(self):
		self.remove_duplicate_addons()
		self.calculate_total_amount()

	def on_submit(self):
		if self.status != "Boarded":
			frappe.throw(_("Should be status filed equal 'Boarded'"))

	def before_insert(self):
		self.set_random_seat()

	def calculate_total_amount(self):
		total_add_on_amount = sum([item.amount for item in self.add_ons])
		self.total_amount = float(self.flight_price) + total_add_on_amount

	def remove_duplicate_addons(self):
		unique_add_ons = []
		seen_items = set()

		for item in self.add_ons:

			if item.item not in seen_items:
				seen_items.add(item.item)
				unique_add_ons.append(item)

		self.add_ons = unique_add_ons

	def set_random_seat(self):
		random_number = random.randint(1, 99)
		random_letter = random.choice(['A', 'B', 'C', 'D', 'E'])
		self.seat = f"{random_number}{random_letter}"
