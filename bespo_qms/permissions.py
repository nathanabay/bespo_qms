import frappe

FINANCE_CATEGORIES = [
    "Tax Notices", "Bank Notices", "Letter of Credit (L/C) Advices", "Guarantee Advices",
    "Bank Letters", "Payment Requisitions & Invoicing", "Tax Compliance Declarations"
]
PROCUREMENT_CATEGORIES = [
    "Supplier Quotations & Bids", "Shipping & Freight Notices", "Supplier Non-Conformance Notifications",
    "Supplier Corrective Action Requests (SCAR)", "Purchase Orders (POs)"
]
ENGINEERING_CATEGORIES = [
    "Tender Invitations / Requests for Proposal (RFPs)", "Site / Architect Instructions",
    "Approval Status Letters", "Notices of Award / Notices to Proceed",
    "Tender Submissions", "Requests for Extension of Time (EOT)", "Prequalification Submissions",
    "Technical Submittals", "Requests for Information (RFIs)", "Inspection Requests",
    "Project Handover Letters", "Site Progress Reports", "Equipment Maintenance Schedules"
]
HR_CATEGORIES = [
    "Policy Announcements", "Disciplinary & Corrective Notices"
]

def get_allowed_categories(user):
    roles = frappe.get_roles(user)
    if "System Manager" in roles or "QMS Executive" in roles:
        return "ALL"
    
    allowed = ["Other", "Letter", "Notice", "Invoice", "Report", "Proposal", "Quote"] # Fallbacks
    if "QMS Finance" in roles: allowed.extend(FINANCE_CATEGORIES)
    if "QMS Procurement" in roles: allowed.extend(PROCUREMENT_CATEGORIES)
    if "QMS Engineering" in roles: allowed.extend(ENGINEERING_CATEGORIES)
    if "QMS HR" in roles: allowed.extend(HR_CATEGORIES)
    
    # Generic QMS User has access to generic stuff plus anything explicit above if they have multi-roles
    
    return allowed

def _build_query(allowed, doctype_name):
    formatted_cats = ", ".join(["%s" for _ in allowed])
    return f"`tab{doctype_name}`.category IN ({formatted_cats})" % tuple(allowed)

def get_incoming_query(user):
    allowed = get_allowed_categories(user)
    if allowed == "ALL":
        return ""
    return _build_query(allowed, "Incoming Document")

def get_outgoing_query(user):
    allowed = get_allowed_categories(user)
    if allowed == "ALL":
        return ""
    return _build_query(allowed, "Outgoing Document")

def get_internal_query(user):
    allowed = get_allowed_categories(user)
    if allowed == "ALL":
        return ""
    return _build_query(allowed, "Internal Document")

def has_qms_permission(doc, ptype, user):
    if not user: user = frappe.session.user
    allowed = get_allowed_categories(user)
    
    if allowed == "ALL":
        return True
        
    if doc.category in allowed:
        return True
        
    # If standard category is somehow not in the list but they created it?
    if doc.owner == user:
        return True
        
    return False
