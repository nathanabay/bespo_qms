# Copyright (c) 2026, BESPO and contributors
# For license information, please see license.txt

import frappe
from frappe.tests.utils import FrappeTestCase


class TestInternalDocument(FrappeTestCase):
    """Tests for Internal Document DocType."""

    def setUp(self):
        """Set up test data."""
        frappe.set_user("Administrator")
        # Create a test category
        if not frappe.db.exists("QMS Document Category", "Test Internal Category"):
            self.test_category = frappe.get_doc({
                "doctype": "QMS Document Category",
                "category_name": "Test Internal Category"
            }).insert()
        else:
            self.test_category = frappe.get_doc("QMS Document Category", "Test Internal Category")

        # Create a test internal document
        self.test_doc = frappe.get_doc({
            "doctype": "Internal Document",
            "subject": "Test Internal Document",
            "category": self.test_category.name,
            "document_date": frappe.utils.today(),
            "content": "This is test content for the internal document.",
            "naming_series": "QMS-INT-.YYYY.-.#####"
        }).insert()
        self.doc_name = self.test_doc.name

    def tearDown(self):
        """Clean up test data."""
        frappe.set_user("Administrator")
        if frappe.db.exists("Internal Document", self.doc_name):
            try:
                frappe.delete_doc("Internal Document", self.doc_name, force=True)
            except Exception:
                pass
        if hasattr(self, "test_category") and frappe.db.exists("QMS Document Category", self.test_category.name):
            try:
                frappe.delete_doc("QMS Document Category", self.test_category.name, force=True)
            except Exception:
                pass
        frappe.db.commit()

    def test_create_internal_document(self):
        """Test creating a new Internal Document."""
        doc = frappe.get_doc({
            "doctype": "Internal Document",
            "subject": "New Internal Policy",
            "category": self.test_category.name,
            "document_date": frappe.utils.today(),
            "content": "Policy content here.",
            "originating_department": "Quality",
            "target_audience": "All Staff",
            "naming_series": "QMS-INT-.YYYY.-.#####"
        })
        doc.insert()
        self.assertTrue(doc.name)
        self.assertEqual(doc.subject, "New Internal Policy")
        self.assertEqual(doc.status, "Draft")

    def test_read_internal_document(self):
        """Test reading an existing Internal Document."""
        doc = frappe.get_doc("Internal Document", self.doc_name)
        self.assertEqual(doc.subject, "Test Internal Document")
        self.assertEqual(doc.status, "Draft")
        self.assertEqual(doc.content, "This is test content for the internal document.")

    def test_update_internal_document(self):
        """Test updating an Internal Document."""
        doc = frappe.get_doc("Internal Document", self.doc_name)
        doc.target_audience = "Management Only"
        doc.save()
        frappe.db.commit()
        updated = frappe.get_doc("Internal Document", self.doc_name)
        self.assertEqual(updated.target_audience, "Management Only")

    def test_internal_document_statuses(self):
        """Test that valid statuses exist."""
        doc = frappe.get_doc("Internal Document", self.doc_name)
        status_field = doc.meta.get_field("status")
        valid_statuses = status_field.options.split("\n")
        self.assertIn("Draft", valid_statuses)
        self.assertIn("Pending", valid_statuses)
        self.assertIn("Approved", valid_statuses)
        self.assertIn("Cancelled", valid_statuses)

    def test_acknowledgements_table(self):
        """Test that acknowledgements table exists."""
        doc = frappe.get_doc("Internal Document", self.doc_name)
        acknowledgements_field = doc.meta.get_field("acknowledgements")
        self.assertEqual(acknowledgements_field.fieldtype, "Table")
        self.assertEqual(acknowledgements_field.options, "Document Acknowledgement")

    def test_amendment_tracking(self):
        """Test that amended_from field exists for amendment tracking."""
        doc = frappe.get_doc("Internal Document", self.doc_name)
        self.assertIn("amended_from", [f.fieldname for f in doc.meta.fields])

    def test_delete_internal_document(self):
        """Test deleting an Internal Document."""
        doc = frappe.get_doc("Internal Document", self.doc_name)
        doc.delete()
        self.assertFalse(frappe.db.exists("Internal Document", self.doc_name))

    def test_before_workflow_action_validation(self):
        """Test that workflow action validation exists in the class."""
        from bespo_qms.bespo_qms.doctype.internal_document.internal_document import InternalDocument
        self.assertTrue(hasattr(InternalDocument, "before_workflow_action"))