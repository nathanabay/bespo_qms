import frappe

def create_workflow_state(state):
    if not frappe.db.exists("Workflow State", state):
        doc = frappe.new_doc("Workflow State")
        doc.workflow_state_name = state
        doc.insert(ignore_permissions=True)
        frappe.db.commit()

def create_workflow_action(action):
    if not frappe.db.exists("Workflow Action Master", action):
        doc = frappe.new_doc("Workflow Action Master")
        doc.workflow_action_name = action
        doc.insert(ignore_permissions=True)
        frappe.db.commit()

def setup_internal_document_workflow():
    frappe.set_user("Administrator")
    
    # Ensure states and actions exist to prevent LinkValidationError
    states = ["Draft", "Pending", "Approved", "Cancelled"]
    actions = ["Request Approval", "Approve", "Reject", "Cancel"]
    
    for s in states:
        create_workflow_state(s)
        
    for a in actions:
        create_workflow_action(a)
    
    # Create the workflow
    if not frappe.db.exists("Workflow", "Internal Document Workflow"):
        wf = frappe.new_doc("Workflow")
        wf.workflow_name = "Internal Document Workflow"
        wf.document_type = "Internal Document"
        wf.is_active = 1
        wf.workflow_state_field = "status"
        
        # States
        wf.append("states", {"state": "Draft", "doc_status": 0, "allow_edit": "QMS User"})
        wf.append("states", {"state": "Pending", "doc_status": 0, "allow_edit": "QMS Executive"})
        wf.append("states", {"state": "Approved", "doc_status": 1, "allow_edit": "QMS Executive", "update_field": "approved_by", "update_value": "User"})
        wf.append("states", {"state": "Cancelled", "doc_status": 2, "allow_edit": "QMS Executive"})
        
        # Transitions
        wf.append("transitions", {"state": "Draft", "action": "Request Approval", "next_state": "Pending", "allowed": "QMS User"})
        wf.append("transitions", {"state": "Pending", "action": "Approve", "next_state": "Approved", "allowed": "QMS Executive"})
        wf.append("transitions", {"state": "Pending", "action": "Reject", "next_state": "Draft", "allowed": "QMS Executive"})
        wf.append("transitions", {"state": "Approved", "action": "Cancel", "next_state": "Cancelled", "allowed": "QMS Executive"})
        
        wf.insert(ignore_permissions=True)
        frappe.db.commit()
        print("Internal Document Workflow created successfully.")
    else:
        print("Internal Document Workflow already exists.")

if __name__ == "__main__":
    setup_internal_document_workflow()
