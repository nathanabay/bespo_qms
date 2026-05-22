# Copyright (c) 2026, BESPO and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now


class InternalDocument(Document):
    def autoname(self):
        """Dynamically generate the Document ID based on Department."""
        from frappe.model.naming import make_autoname

        if self.originating_department:
            dept_prefix = frappe.db.get_value("QMS Department", self.originating_department, "department_code") or "GEN"
        else:
            dept_prefix = "GEN"
            
        self.name = make_autoname(f"QMS-{dept_prefix}-INT-.YYYY.-.####")

    def before_workflow_action(self, workflow_action):
        """Block approval without an attachment — ISO 9001 mandatory documentation compliance."""
        if workflow_action in ("Request Approval", "Approve"):
            attachments = frappe.get_all(
                "File",
                filters={"attached_to_doctype": self.doctype, "attached_to_name": self.name},
                pluck="name"
            )
            if not attachments:
                frappe.throw(
                    "Cannot submit for approval without attaching the policy document. "
                    "Please upload the policy file in the Attachments sidebar.",
                    title="Attachment Required"
                )




    def before_cancel(self):
        """Block cancellation if any user has acknowledged this policy."""
        acknowledged = [r.user for r in self.acknowledgements if r.status == "Acknowledged"]
        if acknowledged:
            frappe.throw(
                f"Cannot cancel: {len(acknowledged)} user(s) have already acknowledged this policy. "
                "Revoke acknowledgements first or contact your System Manager.",
                title="Cancellation Blocked"
            )
