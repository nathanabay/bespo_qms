import frappe

def update_print_format():
    frappe.set_user("Administrator")
    
    print_format_name = "Standard QMS Letter"
    
    if frappe.db.exists("Print Format", print_format_name):
        doc = frappe.get_doc("Print Format", print_format_name)
        doc.html = """
<div class="letter-body" style="font-family: 'Helvetica', 'Arial', sans-serif; font-size: 14px; line-height: 1.6; color: #333;">
    <div style="text-align: right; margin-bottom: 30px;">
        <strong>Date:</strong> {{ doc.get_formatted("document_date") }}<br>
        <strong>Ref:</strong> {{ doc.name }}
    </div>

    <div style="margin-bottom: 40px;">
        <strong>To:</strong><br>
        {{ doc.recipient_name }}<br>
        {% if doc.recipient_email %}<em>{{ doc.recipient_email }}</em><br>{% endif %}
        {% if doc.recipient_reference %}Ref: {{ doc.recipient_reference }}{% endif %}
    </div>

    <div style="margin-bottom: 30px; text-align: center;">
        <h3 style="text-decoration: underline; text-transform: uppercase;">Subject: {{ doc.subject }}</h3>
    </div>

    <div style="margin-bottom: 50px; min-height: 280px;">
        <p>This is a formal communication regarding <strong>{{ doc.category or "General Correspondence" }}</strong>.</p>

        <p>Please find the relevant details linked to:</p>
        <ul>
            {% if doc.customer %}<li>Customer: {{ doc.customer }}</li>{% endif %}
            {% if doc.project %}<li>Project: {{ doc.project }}</li>{% endif %}
            {% if doc.opportunity %}<li>Opportunity: {{ doc.opportunity }}</li>{% endif %}
        </ul>

        {% if doc.opportunity_value or doc.opportunity_close_date or doc.project_deadline %}
        <table style="border-collapse: collapse; width: 100%; margin-top: 20px;">
            <tr style="background: #f5f5f5;">
                <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">Detail</th>
                <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">Value</th>
            </tr>
            {% if doc.opportunity_value %}
            <tr>
                <td style="border: 1px solid #ddd; padding: 8px;">Opportunity Value</td>
                <td style="border: 1px solid #ddd; padding: 8px;">{{ doc.get_formatted("opportunity_value") }}</td>
            </tr>
            {% endif %}
            {% if doc.opportunity_close_date %}
            <tr>
                <td style="border: 1px solid #ddd; padding: 8px;">Expected Close Date</td>
                <td style="border: 1px solid #ddd; padding: 8px;">{{ doc.get_formatted("opportunity_close_date") }}</td>
            </tr>
            {% endif %}
            {% if doc.project_deadline %}
            <tr>
                <td style="border: 1px solid #ddd; padding: 8px;">Project Deadline</td>
                <td style="border: 1px solid #ddd; padding: 8px;">{{ doc.get_formatted("project_deadline") }}</td>
            </tr>
            {% endif %}
        </table>
        {% endif %}

        {% if doc.context_notes %}
        <p style="margin-top:15px; font-style: italic;">{{ doc.context_notes }}</p>
        {% endif %}
    </div>

    <!-- Signature Block -->
    <div style="margin-top: 60px;">
        <p>Yours sincerely,</p>
        {% set approved_user = doc.approved_by or doc.modified_by %}
        {% if approved_user %}
            {% set sig_img = frappe.db.get_value("User", approved_user, "user_image") %}
            {% if sig_img %}
            <div style="margin: 10px 0;">
                <img src="{{ sig_img }}" alt="Signature" style="max-height: 70px; max-width: 200px; object-fit: contain;">
            </div>
            {% endif %}
        {% endif %}
        <br>
        <strong>{{ approved_user or "Management" }}</strong><br>
        Bespo QMS Team
    </div>
</div>
"""
        doc.save(ignore_permissions=True)
        print(f"Print Format '{print_format_name}' updated with digital signature block.")
    else:
        print(f"Print Format '{print_format_name}' not found.")

if __name__ == "__main__":
    update_print_format()
