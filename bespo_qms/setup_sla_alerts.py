import frappe

def setup_sla_alerts():
    frappe.set_user("Administrator")
    
    # Define the Notification for Stagnant Pending Documents
    alert_name = "QMS Stagnant Approval Alert"
    
    if frappe.db.exists("Notification", alert_name):
        frappe.delete_doc("Notification", alert_name, force=True)
        
    doc = frappe.new_doc("Notification")
    doc.name = alert_name
    doc.subject = "Approval Overdue: {{ doc.name }} ({{ doc.department }})"
    doc.document_type = "Outgoing Document"
    doc.event = "Days After"
    doc.date_changed = "modified" # We track from the time it was dragged to Pending (last modified date)
    doc.days_in_advance = -2 # -2 means "2 days AFTER" the date_changed
    doc.condition = "doc.status == 'Pending'"
    
    doc.channel = "Email"
    doc.send_system_notification = 1
    doc.message = """
    <p>Dear QMS Executive,</p>
    <p>The Outgoing Document <b>{{ doc.name }}</b> from the <b>{{ doc.department }}</b> department has been awaiting approval for more than 48 hours.</p>
    <p><b>Category:</b> {{ doc.category }}</p>
    <p><b>Subject:</b> {{ doc.subject }}</p>
    <p>Please review the document here: <a href="/app/outgoing-document/{{ doc.name }}">Review Document</a></p>
    """
    
    # Send it to the QMS Executive role
    doc.append("recipients", {
        "receiver_by_role": "QMS Executive"
    })
    
    doc.insert(ignore_permissions=True)
    frappe.db.commit()
    print(f"Notification '{alert_name}' created successfully.")

if __name__ == "__main__":
    setup_sla_alerts()
