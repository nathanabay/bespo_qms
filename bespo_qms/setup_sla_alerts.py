import frappe

def setup_sla_alerts():

    # Define the Notification for Stagnant Pending Documents
    alert_name = "QMS Stagnant Approval Alert"

    if frappe.db.exists("Notification", alert_name):
        doc = frappe.get_doc("Notification", alert_name)
        # Update only the fields that might have changed
        doc.subject = "Approval Overdue: {{ doc.name }} ({{ doc.department }})"
        doc.document_type = "Outgoing Document"
        doc.event = "Days After"
        doc.date_changed = "modified"
        doc.days_in_advance = 0  # Fire on the day; status==Pending condition gates further
        if doc.condition != "doc.status == 'Pending'":
            doc.condition = "doc.status == 'Pending'"
        doc.message = """
    <p>Dear QMS Executive,</p>
    <p>The Outgoing Document <b>{{ doc.name }}</b> from the <b>{{ doc.department }}</b> department has been awaiting approval for more than 48 hours.</p>
    <p><b>Category:</b> {{ doc.category }}</p>
    <p><b>Subject:</b> {{ doc.subject }}</p>
    <p>Please review the document here: <a href="/app/outgoing-document/{{ doc.name }}">Review Document</a></p>
    """
        doc.channel = "Email"
        doc.send_system_notification = 1
        # Ensure recipients are set
        if not doc.recipients:
            doc.append("recipients", {
                "receiver_by_role": "QMS Executive"
            })
        doc.save(ignore_permissions=True)
    else:
        # Create new
        doc = frappe.new_doc("Notification")
        doc.name = alert_name
        doc.subject = "Approval Overdue: {{ doc.name }} ({{ doc.department }})"
        doc.document_type = "Outgoing Document"
        doc.event = "Days After"
        doc.date_changed = "modified"  # We track from the time it was dragged to Pending (last modified date)
        doc.days_in_advance = 0  # Fire on the day; condition gates the alert
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
        doc.append("recipients", {
            "receiver_by_role": "QMS Executive"
        })
        doc.insert(ignore_permissions=True)
    print(f"Notification '{alert_name}' synced successfully.")

if __name__ == "__main__":
    setup_sla_alerts()