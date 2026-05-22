import frappe
import json

def setup_workspaces_and_submittable():
    
    workspace_name = "Bespo QMS"
    if frappe.db.exists("Workspace", workspace_name):
        frappe.delete_doc("Workspace", workspace_name, force=True)
        print(f"Deleted existing Workspace '{workspace_name}' to rebuild.")
    
    doc = frappe.new_doc("Workspace")
    doc.label = workspace_name
    doc.title = workspace_name
    doc.module = "BESPO_QMS"
    doc.category = "Modules"
    doc.icon = "shield"
    doc.is_hidden = 0
    doc.public = 1

    content_blocks = [
        {"id": "header_analytics", "type": "header", "data": {"text": "<span class=\\\"h4\\\"><b>QMS Analytics</b></span>", "col": 12}},
        {"id": "nc_1", "type": "number_card", "data": {"number_card_name": "Pending Outgoing Approvals", "col": 4}},
        {"id": "nc_2", "type": "number_card", "data": {"number_card_name": "Total Approved Outgoing", "col": 4}},
        {"id": "nc_3", "type": "number_card", "data": {"number_card_name": "Pending Incoming Action", "col": 4}},
        {"id": "ch_1", "type": "chart", "data": {"chart_name": "Outgoing Documents by Department", "col": 6}},
        {"id": "ch_2", "type": "chart", "data": {"chart_name": "Internal Policies by Category", "col": 6}},
        {"id": "spacer_0", "type": "spacer", "data": {"col": 12}},
        {"id": "header_shortcuts", "type": "header", "data": {"text": "<span class=\\\"h4\\\"><b>General Access</b></span>", "col": 12}},
        {"id": "sc_in", "type": "shortcut", "data": {"shortcut_name": "All Incoming", "col": 4}},
        {"id": "sc_out", "type": "shortcut", "data": {"shortcut_name": "All Outgoing", "col": 4}},
        {"id": "sc_int", "type": "shortcut", "data": {"shortcut_name": "All Internal", "col": 4}},
        
        {"id": "spacer_1", "type": "spacer", "data": {"col": 12}},
        {"id": "header_boards", "type": "header", "data": {"text": "<span class=\\\"h4\\\"><b>Department Approval Boards</b></span>", "col": 12}},
        {"id": "kb_fin", "type": "shortcut", "data": {"shortcut_name": "Finance Approvals", "col": 3}},
        {"id": "kb_pro", "type": "shortcut", "data": {"shortcut_name": "Procurement Approvals", "col": 3}},
        {"id": "kb_eng", "type": "shortcut", "data": {"shortcut_name": "Engineering Approvals", "col": 3}},
        {"id": "kb_hr", "type": "shortcut", "data": {"shortcut_name": "HR Approvals", "col": 3}},

        {"id": "spacer_2", "type": "spacer", "data": {"col": 12}},
        {"id": "header_masters", "type": "header", "data": {"text": "<span class=\\\"h4\\\"><b>Masters &amp; Settings</b></span>", "col": 12}},
        {"id": "sc_m1", "type": "shortcut", "data": {"shortcut_name": "Outgoing Documents", "col": 3}},
        {"id": "sc_m2", "type": "shortcut", "data": {"shortcut_name": "Incoming Documents", "col": 3}},
        {"id": "sc_m3", "type": "shortcut", "data": {"shortcut_name": "Internal Documents", "col": 3}},
        {"id": "sc_m5", "type": "shortcut", "data": {"shortcut_name": "QMS Department", "col": 3}},
        {"id": "sc_m6", "type": "shortcut", "data": {"shortcut_name": "QMS Document Category", "col": 3}},
        {"id": "sc_m7", "type": "shortcut", "data": {"shortcut_name": "QMS External Entity", "col": 3}},
        {"id": "sc_m4", "type": "shortcut", "data": {"shortcut_name": "QMS Print Formats", "col": 3}}
    ]
    doc.content = json.dumps(content_blocks)

    # General Shortcuts
    doc.append("shortcuts", {
        "label": "All Incoming",
        "type": "DocType",
        "link_to": "Incoming Document",
        "color": "Grey"
    })
    doc.append("shortcuts", {
        "label": "All Outgoing",
        "type": "DocType",
        "link_to": "Outgoing Document",
        "color": "Grey"
    })
    doc.append("shortcuts", {
        "label": "All Internal",
        "type": "DocType",
        "link_to": "Internal Document",
        "color": "Grey"
    })
    
    # Departmental Kanban Board Shortcuts
    doc.append("shortcuts", {
        "label": "Finance Approvals",
        "type": "DocType",
        "link_to": "Outgoing Document",
        "doc_view": "Kanban",
        "kanban_board": "Finance Approvals",
        "color": "Blue"
    })
    doc.append("shortcuts", {
        "label": "Procurement Approvals",
        "type": "DocType",
        "link_to": "Outgoing Document",
        "doc_view": "Kanban",
        "kanban_board": "Procurement Approvals",
        "color": "Green"
    })
    doc.append("shortcuts", {
        "label": "Engineering Approvals",
        "type": "DocType",
        "link_to": "Outgoing Document",
        "doc_view": "Kanban",
        "kanban_board": "Engineering Approvals",
        "color": "Purple"
    })
    doc.append("shortcuts", {
        "label": "HR Approvals",
        "type": "DocType",
        "link_to": "Internal Document",
        "doc_view": "Kanban",
        "kanban_board": "HR Approvals",
        "color": "Red"
    })

    # Masters & Settings shortcuts (these are the actual rendered items)
    for sc_label, sc_link in [
        ("Outgoing Documents", "Outgoing Document"),
        ("Incoming Documents", "Incoming Document"),
        ("Internal Documents", "Internal Document"),
        ("QMS Department", "QMS Department"),
        ("QMS Document Category", "QMS Document Category"),
        ("QMS External Entity", "QMS External Entity"),
        ("QMS Print Formats", "Print Format"),
    ]:
        doc.append("shortcuts", {
            "label": sc_label,
            "type": "DocType",
            "link_to": sc_link,
            "color": "Orange"
        })

    # --- Populate number_cards child table ---
    for nc_name in ["Pending Outgoing Approvals", "Total Approved Outgoing", "Pending Incoming Action"]:
        doc.append("number_cards", {"number_card_name": nc_name})

    # --- Populate charts child table ---
    for chart_name in ["Outgoing Documents by Department", "Internal Policies by Category"]:
        doc.append("charts", {"chart_name": chart_name})

    doc.insert(ignore_permissions=True)
    print(f"Workspace '{workspace_name}' mapped to Kanban Boards successfully.")

if __name__ == "__main__":
    setup_workspaces_and_submittable()
