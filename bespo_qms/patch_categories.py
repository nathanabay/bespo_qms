import frappe

def patch_category_validation():
    frappe.set_user("Administrator")
    
    # We need to explicitly allow ALL ISO 9001 categories in the backend schema 
    # so that the UI can freely switch between them without throwing ValidationError.
    
    finance_cats = ["", "Tax Notices", "Bank Notices", "Letter of Credit (L/C) Advices", "Guarantee Advices", "Bank Letters", "Payment Requisitions & Invoicing", "Tax Compliance Declarations"]
    procurement_cats = ["Supplier Quotations & Bids", "Shipping & Freight Notices", "Supplier Non-Conformance Notifications", "Supplier Corrective Action Requests (SCAR)", "Purchase Orders (POs)"]
    engineering_cats = ["Tender Invitations / Requests for Proposal (RFPs)", "Site / Architect Instructions", "Approval Status Letters", "Notices of Award / Notices to Proceed", "Tender Submissions", "Requests for Extension of Time (EOT)", "Prequalification Submissions", "Technical Submittals", "Requests for Information (RFIs)", "Inspection Requests", "Project Handover Letters", "Site Progress Reports", "Equipment Maintenance Schedules"]
    hr_cats = ["Policy Announcements", "Disciplinary & Corrective Notices"]
    default_cats = ["Other", "Letter", "Notice", "Invoice", "Report", "Proposal", "Quote"]
    
    all_cats = finance_cats + procurement_cats + engineering_cats + hr_cats + default_cats
    # Remove duplicates, keep order roughly
    unique_cats = list(dict.fromkeys(all_cats))
    
    options_string = "\\n".join(unique_cats)
    
    # Update Incoming Document
    if frappe.db.exists("DocField", {"parent": "Incoming Document", "fieldname": "category"}):
        frappe.db.set_value("DocField", {"parent": "Incoming Document", "fieldname": "category"}, "options", options_string)
        print("Updated core category schema for Incoming Document.")
        
    # Update Outgoing Document
    if frappe.db.exists("DocField", {"parent": "Outgoing Document", "fieldname": "category"}):
        frappe.db.set_value("DocField", {"parent": "Outgoing Document", "fieldname": "category"}, "options", options_string)
        print("Updated core category schema for Outgoing Document.")
        
    frappe.db.commit()

if __name__ == "__main__":
    patch_category_validation()
