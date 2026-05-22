# Copyright (c) 2026, BESPO and contributors
# For license information, please see license.txt

import frappe
from frappe.tests.utils import FrappeTestCase


class TestIncomingDocument(FrappeTestCase):
    """Tests for Incoming Document DocType."""

    def setUp(self):
        """Set up test data."""
        frappe.set_user("Administrator")
        # Create a test category
        if not frappe.db.exists("QMS Document Category", "Test Incoming Category"):
            self.test_category = frappe.get_doc({
                "doctype": "QMS Document Category",
                "category_name": "Test Incoming Category"
            }).insert()
        else:
            self.test_category = frappe.get_doc("QMS Document Category", "Test Incoming Category")

        # Create a test incoming document
        self.test_doc = frappe.get_doc({
            "doctype": "Incoming Document",
            "subject": "Test Incoming Document",
            "sender_name": "Test Sender",
            "document_date": frappe.utils.today(),
            "category": self.test_category.name,
            "naming_series": "QMS-INC-.YYYY.-.#####"
        }).insert()
        self.doc_name = self.test_doc.name

    def tearDown(self):
        """Clean up test data."""
        frappe.set_user("Administrator")
        if frappe.db.exists("Incoming Document", self.doc_name):
            frappe.delete_doc("Incoming Document", self.doc_name, force=True)
        if hasattr(self, "test_category") and frappe.db.exists("QMS Document Category", self.test_category.name):
            try:
                frappe.delete_doc("QMS Document Category", self.test_category.name, force=True)
            except Exception:
                pass
        frappe.db.commit()

    def test_create_incoming_document(self):
        """Test creating a new Incoming Document."""
        doc = frappe.get_doc({
            "doctype": "Incoming Document",
            "subject": "New Incoming Document",
            "sender_name": "External Sender",
            "document_date": frappe.utils.today(),
            "sender_reference": "REF-001",
            "naming_series": "QMS-INC-.YYYY.-.#####"
        })
        doc.insert()
        self.assertTrue(doc.name)
        self.assertEqual(doc.subject, "New Incoming Document")
        self.assertEqual(doc.status, "Draft")

    def test_read_incoming_document(self):
        """Test reading an existing Incoming Document."""
        doc = frappe.get_doc("Incoming Document", self.doc_name)
        self.assertEqual(doc.subject, "Test Incoming Document")
        self.assertEqual(doc.sender_name, "Test Sender")
        self.assertEqual(doc.status, "Draft")

    def test_update_incoming_document(self):
        """Test updating an Incoming Document."""
        doc = frappe.get_doc("Incoming Document", self.doc_name)
        doc.sender_reference = "UPD-REF"
        doc.save()
        frappe.db.commit()
        updated = frappe.get_doc("Incoming Document", self.doc_name)
        self.assertEqual(updated.sender_reference, "UPD-REF")

    def test_incoming_document_statuses(self):
        """Test that valid statuses exist."""
        doc = frappe.get_doc("Incoming Document", self.doc_name)
        status_field = doc.meta.get_field("status")
        valid_statuses = status_field.options.split("\n")
        self.assertIn("Draft", valid_statuses)
        self.assertIn("Pending", valid_statuses)
        self.assertIn("Actioned", valid_statuses)
        self.assertIn("Archived", valid_statuses)

    def test_delete_incoming_document(self):
        """Test deleting an Incoming Document."""
        doc = frappe.get_doc("Incoming Document", self.doc_name)
        doc.delete()
        self.assertFalse(frappe.db.exists("Incoming Document", self.doc_name))

    def test_amendment_tracking(self):
        """Test that amended_from field exists for amendment tracking."""
        doc = frappe.get_doc("Incoming Document", self.doc_name)
        self.assertIn("amended_from", [f.fieldname for f in doc.meta.fields])