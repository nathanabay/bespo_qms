import frappe

def create_roles_and_letterhead():
    frappe.set_user("Administrator")
    
    # 1. Create Roles
    roles = ["QMS User", "QMS Executive"]
    for role in roles:
        if not frappe.db.exists("Role", role):
            frappe.get_doc({
                "doctype": "Role",
                "role_name": role,
                "desk_access": 1
            }).insert(ignore_permissions=True)
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
        }).insert(ignore_permissions=True)
        print(f"Letterhead {letterhead_name} created.")

    # 3. Create Print Format for Outgoing Document
    print_format_name = "Standard QMS Letter"
    if not frappe.db.exists("Print Format", print_format_name):
        frappe.get_doc({
            "doctype": "Print Format",
            "name": print_format_name,
            "doc_type": "Outgoing Document",
            "module": "BESPO_QMS",
            "standard": "No",
            "print_format_type": "Jinja",
            "html": """
<div class="letter-body" style="font-family: 'Helvetica', 'Arial', sans-serif; font-size: 14px; line-height: 1.6; color: #333;">
    <div style="text-align: right; margin-bottom: 30px;">
        <strong>Date:</strong> {{ doc.get_formatted("document_date") }}<br>
        <strong>Ref:</strong> {{ doc.name }}
    </div>

    <div style="margin-bottom: 40px;">
        <strong>To:</strong><br>
        {{ doc.recipient_name }}<br>
        {% if doc.recipient_reference %}
            Ref: {{ doc.recipient_reference }}
        {% endif %}
    </div>

    <div style="margin-bottom: 30px; text-align: center;">
        <h3 style="text-decoration: underline; text-transform: uppercase;">Subject: {{ doc.subject }}</h3>
    </div>

    <div style="margin-bottom: 50px; min-height: 300px;">
        <!-- document content would go here if we had a clear data field for it, 
             for now we use subject and category as context -->
        <p>This is a formal communication regarding <strong>{{ doc.category }}</strong>.</p>
        
        <p>Please find the relevant details linked to:</p>
        <ul>
            {% if doc.customer %}<li>Customer: {{ doc.customer }}</li>{% endif %}
            {% if doc.project %}<li>Project: {{ doc.project }}</li>{% endif %}
            {% if doc.opportunity %}<li>Opportunity: {{ doc.opportunity }}</li>{% endif %}
        </ul>
    </div>

    <div style="margin-top: 60px;">
        <p>Yours sincerely,</p>
        <br><br>
        <strong>Management</strong><br>
        Bespo QMS Team
    </div>
</div>
            """
        }).insert(ignore_permissions=True)
        print(f"Print Format {print_format_name} created.")

    frappe.db.commit()

if __name__ == "__main__":
    create_roles_and_letterhead()
