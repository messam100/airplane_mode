import frappe
from frappe.utils import nowdate

def send_rent_reminders():
    # print("Work")
    # bench execute airplane_mode.airport_shop.utils.scheduler_events.send_rent_reminders TO RUN
    settings = frappe.get_single("Shop Settings")
    if not settings.enable_rent_reminder:
        return

    tenants = frappe.get_all("Tenant", fields=["tenant_name", "email"])
    for tenant in tenants:
        if tenant.email:
            frappe.sendmail(
                recipients=[tenant.email],
                subject="Monthly Rent Reminder",
                message=f"Dear {tenant.tenant_name}, this is a reminder to pay your rent for {nowdate()}."
            )
