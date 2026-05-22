import frappe

def setup_email_notification():
    frappe.set_user("Administrator")
    
    notification_name = "Outgoing Document Approved"
    
    if not frappe.db.exists("Notification", notification_name):
        doc = frappe.new_doc("Notification")
        doc.name = notification_name
        doc.subject = "Approved Notification: {{ doc.subject }}"
        doc.document_type = "Outgoing Document"
        
        # Trigger Conditions
        doc.event = "Value Change"
        doc.value_changed = "status"
        doc.condition = "doc.status == 'Approved'"
        
        # Action
        doc.send_email = 1
        # Leave Sender empty to use the system default email account, or use a valid existing User email.
        doc.sender = "" 
        doc.sender_email = ""
        
        # Recipients
        doc.append("recipients", {
            "receiver_by_document_field": "recipient_email"
        })
        
        # Email Body
        doc.message = """
        <p>Dear {{ doc.recipient_name }},</p>
        
        <p>Your document regarding <strong>{{ doc.subject }}</strong> has been formally approved.</p>
        <p>Please find the official correspondence attached to this email.</p>
        
        <p>Best Regards,<br>Bespo QMS</p>
        """
        
        # Attach Print
        doc.attach_print = 1
        doc.print_format = "Standard QMS Letter"
        
        doc.insert(ignore_permissions=True)
        print(f"Notification '{notification_name}' created successfully.")
    else:
        print(f"Notification '{notification_name}' already exists.")

if __name__ == "__main__":
    setup_email_notification()
