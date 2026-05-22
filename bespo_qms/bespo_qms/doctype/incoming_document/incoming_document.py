# Copyright (c) 2026, Antigravity/Nathanamare and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class IncomingDocument(Document):
	def autoname(self):
		"""Dynamically generate the Document ID based on Department."""
		from frappe.model.naming import make_autoname
		
		if self.department:
			dept_prefix = frappe.db.get_value("QMS Department", self.department, "department_code") or "GEN"
		else:
			dept_prefix = "GEN"
		
		self.name = make_autoname(f"QMS-{dept_prefix}-IN-.YYYY.-.####")

	def before_workflow_action(self, workflow_action):
		"""Block actioning without an attachment — ISO 9001 mandatory documentation compliance."""
		if workflow_action == "Complete":
			attachments = frappe.get_all(
				"File",
				filters={"attached_to_doctype": self.doctype, "attached_to_name": self.name},
				pluck="name"
			)
			if not attachments:
				frappe.throw(
					"Cannot mark as Actioned without attaching the original document. "
					"Please upload the letter or file in the Attachments sidebar.",
					title="Attachment Required"
				)
