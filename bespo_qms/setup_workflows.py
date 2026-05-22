import frappe

def create_workflows():
    frappe.set_user("Administrator")
    
    # 1. Create Workflow States
    required_states = ["Draft", "Pending", "Approved", "Dispatched", "Cancelled", "Actioned"]
    for state in required_states:
        if not frappe.db.exists("Workflow State", state):
            frappe.get_doc({
                "doctype": "Workflow State",
                "workflow_state_name": state
            }).insert(ignore_permissions=True)
            print(f"Workflow State {state} created.")

    # 2. Create Workflow Actions (required for Transitions)
    required_actions = ["Submit for Approval", "Approve", "Reject", "Dispatch", "Cancel", "Complete", "Mark as Pending"]
    for action in required_actions:
        if not frappe.db.exists("Workflow Action Master", action):
            frappe.get_doc({
                "doctype": "Workflow Action Master",
                "workflow_action_name": action
            }).insert(ignore_permissions=True)
            print(f"Workflow Action {action} created.")

    # 3. Create Outgoing Workflow (idempotent - check and update, don't delete/recreate)
    workflow_name = "Outgoing Document Approval"
    if not frappe.db.exists("Workflow", workflow_name):
        doc = frappe.new_doc("Workflow")
        doc.workflow_name = workflow_name
        doc.document_type = "Outgoing Document"
        doc.workflow_state_field = "status"
        doc.is_active = 1
        doc.override_status = 1

        doc.append("states", {"state": "Draft", "allow_edit": "System Manager", "doc_status": "0"})
        doc.append("states", {"state": "Pending", "allow_edit": "System Manager", "doc_status": "0", "update_field": "", "update_value": ""})
        doc.append("states", {"state": "Approved", "allow_edit": "System Manager", "doc_status": "1", "update_field": "approved_by", "update_value": ""})
        doc.append("states", {"state": "Dispatched", "allow_edit": "System Manager", "doc_status": "1"})
        doc.append("states", {"state": "Cancelled", "allow_edit": "System Manager", "doc_status": "2"})

        doc.append("transitions", {"state": "Draft", "action": "Submit for Approval", "next_state": "Pending", "allowed": "System Manager"})
        doc.append("transitions", {"state": "Pending", "action": "Approve", "next_state": "Approved", "allowed": "System Manager"})
        doc.append("transitions", {"state": "Pending", "action": "Reject", "next_state": "Draft", "allowed": "System Manager"})
        doc.append("transitions", {"state": "Approved", "action": "Dispatch", "next_state": "Dispatched", "allowed": "System Manager"})
        doc.append("transitions", {"state": "Approved", "action": "Cancel", "next_state": "Cancelled", "allowed": "System Manager"})

        doc.insert(ignore_permissions=True)
        print(f"Workflow {workflow_name} created.")
    else:
        print(f"Workflow {workflow_name} already exists, skipping.")

    # 4. Create Incoming Workflow
    workflow_name = "Incoming Document Workflow"
    if not frappe.db.exists("Workflow", workflow_name):
        doc = frappe.new_doc("Workflow")
        doc.workflow_name = workflow_name
        doc.document_type = "Incoming Document"
        doc.workflow_state_field = "status"
        doc.is_active = 1
        doc.override_status = 1

        doc.append("states", {"state": "Draft", "allow_edit": "QMS Executive", "doc_status": "0"})
        doc.append("states", {"state": "Actioned", "allow_edit": "QMS Executive", "doc_status": "1"})

        doc.append("transitions", {"state": "Draft", "action": "Complete", "next_state": "Actioned", "allowed": "QMS Executive"})

        doc.insert(ignore_permissions=True)
        print(f"Workflow {workflow_name} created.")

if __name__ == "__main__":
    create_workflows()
