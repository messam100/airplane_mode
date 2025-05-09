# Copyright (c) 2025, Mohammed Al-Qershi and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator


class AirplaneFlight(WebsiteGenerator):
	def on_submit(self):
		self.status = "Completed"
		self.submit_boarded_tickets()
  
	def after_insert(self):
		frappe.enqueue("airplane_mode.airplane_mode.doctype.airplane_flight.airplane_flight.create_seats", flight_name=self.name)
  
	def submit_boarded_tickets(self):
		tickets = frappe.get_all("Airplane Ticket", filters={
    	    "flight": self.name,
    	    "status": "Boarded",
    	    "docstatus": 0
    	})

		for ticket in tickets:
			ticket_doc = frappe.get_doc("Airplane Ticket", ticket.name)
			ticket_doc.submit()

def create_seats(flight_name):
    #TODO: Take Max Number Form Capacity (Airplane Doctype)
	seat_rows = range(1, 21)
	seat_columns = ['A', 'B', 'C', 'D', 'E', 'F']
	for row in seat_rows:
		for col in seat_columns:
			seat = frappe.new_doc("Airplane Seat")
			seat.seat_number = f"{row}{col}"
			seat.airplane_flight = flight_name
			seat.status = "Available"
			seat.insert(ignore_permissions=True)
