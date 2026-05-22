import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_field

def add_department_fields():
    options = "Finance\nProcurement\nEngineering\nHR\nOther"
    
    # 1. Incoming Document
    create_custom_field(
        "Incoming Document",
        {
            "fieldname": "department",
            "label": "Department",
            "fieldtype": "Select",
            "options": options,
            "insert_after": "document_date",
            "reqd": 1,
            "in_list_view": 1,
            "in_standard_filter": 1
        }
    )
    print("Added department to Incoming Document.")

    # 2. Outgoing Document
    create_custom_field(
        "Outgoing Document",
        {
            "fieldname": "department",
            "label": "Department",
            "fieldtype": "Select",
            "options": options,
            "insert_after": "document_date",
            "reqd": 1,
            "in_list_view": 1,
            "in_standard_filter": 1
        }
    )
    print("Added department to Outgoing Document.")

    # 3. Internal Document (Change originating_department -> department)
    # We will just add the standard department field, and remove the custom originating_department
    if frappe.db.exists("Custom Field", "Internal Document-originating_department"):
        frappe.delete_doc("Custom Field", "Internal Document-originating_department")
        print("Removed old originating_department from Internal Document")
        
    create_custom_field(
        "Internal Document",
        {
            "fieldname": "department",
            "label": "Department",
            "fieldtype": "Select",
            "options": options,
            "insert_after": "document_date",
            "reqd": 1,
            "in_list_view": 1,
            "in_standard_filter": 1
        }
    )
    print("Added standard department to Internal Document.")

if __name__ == "__main__":
    add_department_fields()
