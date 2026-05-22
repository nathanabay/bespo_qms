import frappe
import json

def setup_dashboards():
    frappe.set_user("Administrator")
    
    # --- 1. Create Number Cards ---
    cards = [
        {
            "name": "Pending Outgoing Approvals",
            "doctype": "Outgoing Document",
            "function": "Count",
            "filters": '[["Outgoing Document","status","=","Pending"]]',
            "color": "#ff8c00" # Orange
        },
        {
            "name": "Total Approved Outgoing",
            "doctype": "Outgoing Document",
            "function": "Count",
            "filters": '[["Outgoing Document","status","=","Approved"]]',
            "color": "#2e8b57" # SeaGreen
        },
        {
            "name": "Pending Incoming Action",
            "doctype": "Incoming Document",
            "function": "Count",
            "filters": '[["Incoming Document","status","=","Draft"]]',
            "color": "#dc143c" # Crimson
        }
    ]

    for c in cards:
        if frappe.db.exists("Number Card", c["name"]):
            frappe.delete_doc("Number Card", c["name"], force=True)
            
        doc = frappe.new_doc("Number Card")
        doc.label = c["name"]
        doc.document_type = c["doctype"]
        doc.function = c["function"]
        doc.filters_json = c["filters"]
        doc.color = c["color"]
        doc.is_standard = 1
        doc.module = "BESPO_QMS"
        doc.is_public = 1
        doc.insert(ignore_permissions=True)
        print(f"Number Card '{c['name']}' created.")

    # --- 2. Create Dashboard Charts ---
    charts = [
        {
            "name": "Outgoing Documents by Department",
            "chart_type": "Group By",
            "document_type": "Outgoing Document",
            "group_by_type": "Count",
            "group_by_based_on": "department",
            "type": "Donut",
            "color": "#1f77b4"
        },
        {
            "name": "Internal Policies by Category",
            "chart_type": "Group By",
            "document_type": "Internal Document",
            "group_by_type": "Count",
            "group_by_based_on": "category",
            "type": "Bar",
            "color": "#9467bd"
        }
    ]

    for ch in charts:
        if frappe.db.exists("Dashboard Chart", ch["name"]):
            frappe.delete_doc("Dashboard Chart", ch["name"], force=True)
            
        doc = frappe.new_doc("Dashboard Chart")
        doc.chart_name = ch["name"]
        doc.chart_type = ch["chart_type"]
        doc.document_type = ch["document_type"]
        doc.group_by_type = ch["group_by_type"]
        doc.group_by_based_on = ch["group_by_based_on"]
        doc.type = ch["type"]
        doc.color = ch["color"]
        doc.filters_json = "{}"
        doc.is_standard = 1
        doc.module = "BESPO_QMS"
        doc.is_public = 1
        doc.insert(ignore_permissions=True)
        print(f"Dashboard Chart '{ch['name']}' created.")

    frappe.db.commit()

if __name__ == "__main__":
    setup_dashboards()
