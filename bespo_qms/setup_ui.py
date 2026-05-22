import frappe

def create_roles_and_letterhead():
    # Use frappe's setup flag to bypass permissions for installation/setup scripts
    # This is the documented Frappe approach for setup scripts vs the anti-pattern
    # of using frappe.set_user("Administrator") with ignore_permissions=True
    original_flag = frappe.flags.get("ignore_account_permission", False)
    frappe.flags.ignore_account_permission = True

    try:
        # 1. Create Roles
        roles = ["QMS User", "QMS Executive"]
        for role in roles:
            if not frappe.db.exists("Role", role):
                frappe.get_doc({
                    "doctype": "Role",
                    "role_name": role,
                    "desk_access": 1
                }).insert()
                print(f"Role {role} created.")

        # 2. Create Letterhead
        letterhead_name = "Bespo QMS Letterhead"
        if not frappe.db.exists("Letter Head", letterhead_name):
            frappe.get_doc({
                "doctype": "Letter Head",
                "letter_head_name": letterhead_name,
                "header_html": "<div style='text-align: center; border-bottom: 2px solid #000; padding-bottom: 20px;'><h1 style='margin: 0; color: #1a1a1a;'>BESPO QMS</h1><p style='margin: 5px 0;'>Documented Information System / ISO 9001:2015</p></div>",
                "footer_html": "<div style='text-align: center; font-size: 10px; color: #666; border-top: 1px solid #ccc; padding-top: 10px;'><p>Standardized correspondence generated via Bespo QMS Module</p></div>",
                "is_default": 1
            }).insert()
            print(f"Letterhead {letterhead_name} created.")

        frappe.db.commit()
    finally:
        # Restore original flag state
        frappe.flags.ignore_account_permission = original_flag

if __name__ == "__main__":
    create_roles_and_letterhead()
