import frappe
from frappe.desk.doctype.kanban_board.kanban_board import get_kanban_boards

def force_kanban_columns():
    frappe.set_user("Administrator")

    boards = ["Finance Approvals", "Procurement Approvals", "Engineering Approvals", "HR Approvals"]

    for b in boards:
        doc = frappe.get_doc("Kanban Board", b)
        
        # Clear existing just in case
        doc.columns = []
        
        columns_to_add = [
            {"column_name": "Draft", "status": "Active", "indicator": "Gray"},
            {"column_name": "Pending", "status": "Active", "indicator": "Orange"},
            {"column_name": "Approved", "status": "Active", "indicator": "Green"},
            {"column_name": "Cancelled", "status": "Active", "indicator": "Red"}
        ]
        
        if doc.reference_doctype == "Outgoing Document":
            # Insert Dispatched before Cancelled
            columns_to_add.insert(3, {"column_name": "Dispatched", "status": "Active", "indicator": "Light Blue"})

        for col in columns_to_add:
            doc.append("columns", col)
            
        doc.save(ignore_permissions=True)
        print(f"Forced column save for {b}")

    frappe.db.commit()

if __name__ == "__main__":
    force_kanban_columns()
