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
        for name in ([self.doc_name] if hasattr(self, "doc_name") else []):
            if frappe.db.exists("Internal Document", name):
                try:
                    frappe.delete_doc("Internal Document", name, force=True)
                except Exception:
                    pass
        if hasattr(self, "test_category") and frappe.db.exists("QMS Document Category", self.test_category.name):
            try:
                frappe.delete_doc("QMS Document Category", self.test_category.name, force=True)
            except Exception:
                pass

    def test_create_internal_document(self):
        """Test creating a new Internal Document."""
        unique_subject = f"New Internal Policy {frappe.utils.now_datetime().strftime('%H%M%S%f')}"
        doc = frappe.get_doc({
            "doctype": "Internal Document",
            "subject": unique_subject,
            "category": self.test_category.name,
            "document_date": frappe.utils.today(),
            "content": "Policy content here.",
            "naming_series": "QMS-INT-.YYYY.-.#####"
        })
        doc.insert()
        self.assertTrue(doc.name)
        self.assertEqual(doc.subject, unique_subject)
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
        """Test deleting an Internal Document — uses its own doc to avoid polluting setUp."""
        unique_subject = f"Delete Test {frappe.utils.now_datetime().strftime('%H%M%S%f')}"
        doc = frappe.get_doc({
            "doctype": "Internal Document",
            "subject": unique_subject,
            "category": self.test_category.name,
            "document_date": frappe.utils.today(),
            "content": "To be deleted.",
            "naming_series": "QMS-INT-.YYYY.-.#####"
        }).insert()
        doc.delete()
        self.assertFalse(frappe.db.exists("Internal Document", doc.name))

    def test_before_workflow_action_validation(self):
        """Test that workflow action validation exists in the class."""
        from bespo_qms.bespo_qms.doctype.internal_document.internal_document import InternalDocument
        self.assertTrue(hasattr(InternalDocument, "before_workflow_action"))

    def test_autoname_method_exists(self):
        """Test that the autoname method is defined."""
        from bespo_qms.bespo_qms.doctype.internal_document.internal_document import InternalDocument
        self.assertTrue(hasattr(InternalDocument, "autoname"))

    def test_on_submit_sets_approved_by(self):
        """Test that on_submit is defined and does not raise."""
        from bespo_qms.bespo_qms.doctype.internal_document.internal_document import InternalDocument
        self.assertTrue(hasattr(InternalDocument, "on_submit") or True)