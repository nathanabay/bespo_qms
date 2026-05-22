import frappe
from frappe.desk.doctype.kanban_board.kanban_board import add_column

def create_kanban():
    boards = [
        {
            "name": "Finance Approvals",
            "doctype": "Outgoing Document"
        },
        {
            "name": "Procurement Approvals",
            "doctype": "Outgoing Document"
        },
        {
            "name": "Engineering Approvals",
            "doctype": "Outgoing Document"
        },
        {
            "name": "HR Approvals",
            "doctype": "Internal Document"
        }
    ]

    for b in boards:
        if frappe.db.exists("Kanban Board", b["name"]):
            print(f"Kanban Board '{b['name']}' already exists, skipping.")
        else:
            doc = frappe.new_doc("Kanban Board")
            doc.kanban_board_name = b["name"]
            doc.reference_doctype = b["doctype"]
            doc.field_name = "status"
            doc.private = 0
            doc.fields = '["name","subject","category","status","document_date"]'
            # Set department-based filters so board members only see records for their department
            if b["name"] == "Finance Approvals":
                doc.filters = '[["Outgoing Document","department","=","Finance"]]'
            elif b["name"] == "Procurement Approvals":
                doc.filters = '[["Outgoing Document","department","=","Procurement"]]'
            elif b["name"] == "Engineering Approvals":
                doc.filters = '[["Outgoing Document","department","=","Engineering"]]'
            elif b["name"] == "HR Approvals":
                doc.filters = '[["Internal Document","originating_department","=","HR"]]'

            doc.insert(ignore_permissions=True)

            # Safely add columns using Frappe's own API
            add_column(b["name"], "Draft")
            add_column(b["name"], "Pending")
            add_column(b["name"], "Approved")

            if b["doctype"] == "Outgoing Document":
                add_column(b["name"], "Dispatched")

            add_column(b["name"], "Cancelled")

            print(f"Kanban Board '{b['name']}' built via API (without conflicting internal filters).")

if __name__ == "__main__":
    create_kanban()
