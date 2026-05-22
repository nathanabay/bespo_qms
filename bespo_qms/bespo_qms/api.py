# Copyright (c) 2026, BESPO and contributors
# For license information, please see license.txt

"""
API endpoints for the BESPO QMS application.

This module contains standalone @frappe.whitelist() API functions used by
QMS documents such as Outgoing Document and Internal Document.
"""

import frappe


# ─── Outgoing Document APIs ────────────────────────────────────────────────


@frappe.whitelist()
def get_opportunity_details(opportunity):
    """Fetch key CRM data from a linked Opportunity."""
    frappe.only_for("Sales Manager")
    if not opportunity:
        return {}
    opp = frappe.get_value(
        "Opportunity",
        opportunity,
        ["opportunity_amount", "expected_closing", "customer_name", "contact_display"],
        as_dict=True,
    )
    return opp or {}


@frappe.whitelist()
def get_project_details(project):
    """Fetch key scheduling data from a linked Project."""
    frappe.only_for("Sales Manager")
    if not project:
        return {}
    proj = frappe.get_value(
        "Project",
        project,
        ["project_name", "expected_end_date", "expected_start_date", "percent_complete"],
        as_dict=True,
    )
    return proj or {}


# ─── Internal Document APIs ─────────────────────────────────────────────────


@frappe.whitelist()
def acknowledge_policy(docname):
    """Record the current user's acknowledgement on an Internal Document."""
    frappe.only_for("QMS User", "QMS Executive", "System Manager")
    from frappe.utils import now

    doc = frappe.get_doc("Internal Document", docname)

    # Check if user has already acknowledged
    for row in doc.acknowledgements:
        if row.user == frappe.session.user and row.status == "Acknowledged":
            frappe.throw("You have already acknowledged this policy.", title="Already Acknowledged")

    # Find existing pending row for this user or append a new one
    existing = next((r for r in doc.acknowledgements if r.user == frappe.session.user), None)
    if existing:
        existing.status = "Acknowledged"
        existing.acknowledged_on = now()
    else:
        doc.append("acknowledgements", {
            "user": frappe.session.user,
            "status": "Acknowledged",
            "acknowledged_on": now()
        })

    doc.save()
    return "Acknowledged"