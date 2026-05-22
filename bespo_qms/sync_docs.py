import frappe
from frappe.modules.utils import sync_customizations

def execute():
    # Force reload all doctypes in Ethiopia Compliance
    try:
        frappe.reload_doc("ethiopia_compliance", "doctype", "wht_certificate")
        print("Reloaded WHT Certificate")
    except Exception as e:
        print("Failed WHT Certificate:", e)

    try:
        frappe.reload_doc("ethiopia_compliance", "doctype", "wht_certificate_invoice")
        print("Reloaded WHT Certificate Invoice")
    except Exception as e:
        print("Failed WHT Certificate Invoice:", e)
        
    frappe.db.commit()
