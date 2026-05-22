# Copyright (c) 2026, BESPO and contributors
# For license information, please see license.txt

import frappe
from frappe.tests.utils import FrappeTestCase


class TestOutgoingDocument(FrappeTestCase):
    """Tests for Outgoing Document DocType."""

    def setUp(self):
        """Set up test data."""
        frappe.set_user("Administrator")
        # Create a test category
        if not frappe.db.exists("QMS Document Category", "Test Outgoing Category"):
            self.test_category = frappe.get_doc({
                "doctype": "QMS Document Category",
                "category_name": "Test Outgoing Category"
            }).insert()
        else:
            self.test_category = frappe.get_doc("QMS Document Category", "Test Outgoing Category")

        # Create a test outgoing document
        self.test_doc = frappe.get_doc({
            "doctype": "Outgoing Document",
            "subject": "Test Outgoing Document",
            "recipient_name": "Test Recipient",
            "recipient_email": "recipient@test.com",
            "document_date": frappe.utils.today(),
            "category": self.test_category.name,
            "naming_series": "QMS-OUT-.YYYY.-.#####"
        }).insert()
        self.doc_name = self.test_doc.name

    def tearDown(self):
        """Clean up test data."""
        frappe.set_user("Administrator")
        if frappe.db.exists("Outgoing Document", self.doc_name):
            try:
                frappe.delete_doc("Outgoing Document", self.doc_name, force=True)
            except Exception:
                pass
        if hasattr(self, "test_category") and frappe.db.exists("QMS Document Category", self.test_category.name):
            try:
                frappe.delete_doc("QMS Document Category", self.test_category.name, force=True)
            except Exception:
                pass
        frappe.db.commit()

    def test_create_outgoing_document(self):
        """Test creating a new Outgoing Document."""
        doc = frappe.get_doc({
            "doctype": "Outgoing Document",
            "subject": "New Outgoing Document",
            "recipient_name": "External Recipient",
            "recipient_email": "external@recipient.com",
            "recipient_reference": "REF-001",
            "document_date": frappe.utils.today(),
            "naming_series": "QMS-OUT-.YYYY.-.#####"
        })
        doc.insert()
        self.assertTrue(doc.name)
        self.assertEqual(doc.subject, "New Outgoing Document")
        self.assertEqual(doc.status, "Draft")

    def test_read_outgoing_document(self):
        """Test reading an existing Outgoing Document."""
        doc = frappe.get_doc("Outgoing Document", self.doc_name)
        self.assertEqual(doc.subject, "Test Outgoing Document")
        self.assertEqual(doc.recipient_name, "Test Recipient")
        self.assertEqual(doc.status, "Draft")

    def test_update_outgoing_document(self):
        """Test updating an Outgoing Document."""
        doc = frappe.get_doc("Outgoing Document", self.doc_name)
        doc.recipient_reference = "UPD-REF"
        doc.save()
        frappe.db.commit()
        updated = frappe.get_doc("Outgoing Document", self.doc_name)
        self.assertEqual(updated.recipient_reference, "UPD-REF")

    def test_outgoing_document_statuses(self):
        """Test that valid statuses exist."""
        doc = frappe.get_doc("Outgoing Document", self.doc_name)
        status_field = doc.meta.get_field("status")
        valid_statuses = status_field.options.split("\n")
        self.assertIn("Draft", valid_statuses)
        self.assertIn("Pending", valid_statuses)
        self.assertIn("Approved", valid_statuses)
        self.assertIn("Dispatched", valid_statuses)
        self.assertIn("Cancelled", valid_statuses)

    def test_context_fields_exist(self):
        """Test that context auto-fill fields exist."""
        doc = frappe.get_doc("Outgoing Document", self.doc_name)
        fieldnames = [f.fieldname for f in doc.meta.fields]
        self.assertIn("opportunity_value", fieldnames)
        self.assertIn("opportunity_close_date", fieldnames)
        self.assertIn("project_deadline", fieldnames)
        self.assertIn("context_notes", fieldnames)

    def test_amendment_tracking(self):
        """Test that amended_from field exists for amendment tracking."""
        doc = frappe.get_doc("Outgoing Document", self.doc_name)
        self.assertIn("amended_from", [f.fieldname for f in doc.meta.fields])

    def test_delete_outgoing_document(self):
        """Test deleting an Outgoing Document."""
        doc = frappe.get_doc("Outgoing Document", self.doc_name)
        doc.delete()
        self.assertFalse(frappe.db.exists("Outgoing Document", self.doc_name))

    def test_before_workflow_action_method_exists(self):
        """Test that workflow action validation exists in the class."""
        from bespo_qms.bespo_qms.doctype.outgoing_document.outgoing_document import OutgoingDocument
        self.assertTrue(hasattr(OutgoingDocument, "before_workflow_action"))