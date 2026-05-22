import frappe
import json

def setup_workspaces():
    setup_ethiopia_compliance()
    setup_iso_quality()
    print("Workspaces configured successfully.")

def setup_ethiopia_compliance():
    workspace_name = "Ethiopia Compliance"
    
    ws_content = [
        {"type": "header", "data": {"text": "Tax & Compliance Tracking", "level": 2, "col": 12}},
        {"type": "shortcut", "data": {"shortcut_name": "WHT Certificates", "col": 6}},
        {"type": "shortcut", "data": {"shortcut_name": "WHT Invoices", "col": 6}}
    ]

    shortcuts = [
        {"link_to": "WHT Certificate", "type": "DocType", "label": "WHT Certificates", "icon": "file", "color": "Blue"},
        {"link_to": "WHT Certificate Invoice", "type": "DocType", "label": "WHT Invoices", "icon": "invoice", "color": "Green"}
    ]

    ws_doc = {
        "doctype": "Workspace",
        "name": workspace_name,
        "label": workspace_name,
        "title": workspace_name,
        "category": "Modules",
        "module": "Ethiopia Compliance",
        "icon": "folder",
        "public": 1,
        "shortcuts": shortcuts,
        "content": json.dumps(ws_content),
        "is_hidden": 0
    }

    upsert_workspace(workspace_name, ws_doc)

def setup_iso_quality():
    workspace_name = "ISO Quality"
    
    ws_content = [
        {"type": "header", "data": {"text": "Quality Control & Assurance", "level": 2, "col": 12}},
        {"type": "shortcut", "data": {"shortcut_name": "ISO CAPA", "col": 4}},
        {"type": "shortcut", "data": {"shortcut_name": "ISO Documents", "col": 4}},
        {"type": "shortcut", "data": {"shortcut_name": "ISO NCR", "col": 4}}
    ]

    shortcuts = [
        {"link_to": "ISO CAPA", "type": "DocType", "label": "ISO CAPA", "icon": "check", "color": "Red"},
        {"link_to": "ISO Document", "type": "DocType", "label": "ISO Documents", "icon": "file", "color": "Blue"},
        {"link_to": "ISO NCR", "type": "DocType", "label": "ISO NCR", "icon": "warning", "color": "Orange"}
    ]

    ws_doc = {
        "doctype": "Workspace",
        "name": workspace_name,
        "label": workspace_name,
        "title": workspace_name,
        "category": "Modules",
        "module": "ISO Quality",
        "icon": "shield",
        "public": 1,
        "shortcuts": shortcuts,
        "content": json.dumps(ws_content),
        "is_hidden": 0
    }

    upsert_workspace(workspace_name, ws_doc)

def upsert_workspace(name, doct):
    if not frappe.db.exists("Workspace", name):
        frappe.get_doc(doct).insert(ignore_permissions=True)
        print(f"✔ Created Workspace: {name}")
    else:
        doc = frappe.get_doc("Workspace", name)
        doc.update(doct)
        doc.save(ignore_permissions=True)
        print(f"✔ Updated Workspace: {name}")

def execute():
    setup_workspaces()
