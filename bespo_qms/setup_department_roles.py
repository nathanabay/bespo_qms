import frappe

def create_role(role_name):
    if not frappe.db.exists("Role", role_name):
        doc = frappe.new_doc("Role")
        doc.role_name = role_name
        doc.insert(ignore_permissions=True)
        print(f"Created role: {role_name}")
    else:
        print(f"Role {role_name} already exists.")

def add_doctype_perms(doctype, role):
    # Check if a custom docperm already exists for this doctype/role
    perm = frappe.db.exists("Custom DocPerm", {"parent": doctype, "role": role})
    if not perm:
        frappe.get_doc({
            "doctype": "Custom DocPerm",
            "parent": doctype,
            "parenttype": "DocType",
            "parentfield": "permissions",
            "role": role,
            "read": 1,
            "write": 1,
            "create": 1,
            "submit": 0
        }).insert(ignore_permissions=True)
        print(f"Added docperm for {doctype} - {role}")

def setup_department_roles():
    roles = ["QMS Finance", "QMS Procurement", "QMS Engineering", "QMS HR"]
    for r in roles:
        create_role(r)
        
    # We need to give these roles standard create/read/write to the DocTypes.
    # The read rows will be heavily restricted by hooks.py permission_query_conditions
    doctypes = ["Incoming Document", "Outgoing Document", "Internal Document"]
    
    for dt in doctypes:
        for r in roles:
            add_doctype_perms(dt, r)
            
    # Also ensure standard QMS User has generic access to Internal Document if we didn't add it in Phase 7
    add_doctype_perms("Internal Document", "QMS User")

if __name__ == "__main__":
    setup_department_roles()
