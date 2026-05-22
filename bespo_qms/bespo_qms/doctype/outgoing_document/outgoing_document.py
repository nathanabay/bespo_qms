# Copyright (c) 2026, Nathanamare and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class OutgoingDocument(Document):

    def autoname(self):
        """Dynamically generate the Document ID based on Department."""
        from frappe.model.naming import make_autoname
        
        if self.department:
            dept_prefix = frappe.db.get_value("QMS Department", self.department, "department_code") or "GEN"
        else:
            dept_prefix = "GEN"
            
        self.name = make_autoname(f"QMS-{dept_prefix}-OUT-.YYYY.-.####")

    def before_workflow_action(self, workflow_action):
        """Block submission if no file is attached — ISO 9001 mandatory documentation compliance."""
        if workflow_action == "Submit for Approval":
            attachments = frappe.get_all(
                "File",
                filters={"attached_to_doctype": self.doctype, "attached_to_name": self.name},
                pluck="name"
            )
            if not attachments:
                frappe.throw(
                    "Cannot submit for approval without attaching a document. "
                    "Please upload the relevant file in the Attachments sidebar.",
                    title="Attachment Required"
                )

    def on_submit(self):
        """Record who approved this document."""
        self.db_set("approved_by", frappe.session.user, notify=True)


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
