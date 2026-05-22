import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_field

def add_department_fields():
    fields = [
        {
            "dt": "Incoming Document",
            "label": "Department",
            "after": "document_date"
        },
        {
            "dt": "Outgoing Document",
            "label": "Department",
            "after": "document_date"
        },
        {
            "dt": "Internal Document",
            "label": "Department",
            "after": "document_date"
        }
    ]

    for f in fields:
        cf_name = f"{f['dt']}-{f['label'].lower()}"
        if frappe.db.exists("Custom Field", cf_name):
            print(f"Custom Field '{cf_name}' already exists, skipping.")
        else:
            create_custom_field(
                f["dt"],
                {
                    "fieldname": f["label"].lower(),
                    "label": f["label"],
                    "fieldtype": "Select",
                    "options": "Finance\nProcurement\nEngineering\nHR\nOther",
                    "insert_after": f["after"],
                    "reqd": 1,
                    "in_list_view": 1,
                    "in_standard_filter": 1
                }
            )
            print(f"Added {f['label']} to {f['dt']}.")

if __name__ == "__main__":
    add_department_fields()