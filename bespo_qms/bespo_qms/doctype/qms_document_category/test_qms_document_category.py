# Copyright (c) 2026, BESPO and contributors
# For license information, please see license.txt

import frappe
from frappe.tests.utils import FrappeTestCase


class TestQMSDocumentCategory(FrappeTestCase):
    """Tests for QMS Document Category DocType."""

    def setUp(self):
        """Set up test data."""
        frappe.set_user("Administrator")
        # Create a test department first (needed for category link)
        if not frappe.db.exists("QMS Department", "Test Dept"):
            self.test_dept = frappe.get_doc({
                "doctype": "QMS Department",
                "department_name": "Test Dept",
                "department_code": "TD"
            }).insert()
        else:
            self.test_dept = frappe.get_doc("QMS Department", "Test Dept")
        # Create a test category
        self.test_category = frappe.get_doc({
            "doctype": "QMS Document Category",
            "category_name": "Test Category",
            "description": "Test description",
            "department": self.test_dept.name
        }).insert()
        self.category_name = self.test_category.name

    def tearDown(self):
        """Clean up test data."""
        frappe.set_user("Administrator")
        if frappe.db.exists("QMS Document Category", self.category_name):
            frappe.delete_doc("QMS Document Category", self.category_name, force=True)
        if hasattr(self, "test_dept") and frappe.db.exists("QMS Department", self.test_dept.name):
            frappe.delete_doc("QMS Department", self.test_dept.name, force=True)
        frappe.db.commit()

    def test_create_category(self):
        """Test creating a new QMS Document Category."""
        cat = frappe.get_doc({
            "doctype": "QMS Document Category",
            "category_name": "Policy Documents",
            "description": "Company policy documents"
        })
        cat.insert()
        self.assertTrue(cat.name)
        self.assertEqual(cat.category_name, "Policy Documents")

    def test_read_category(self):
        """Test reading an existing QMS Document Category."""
        cat = frappe.get_doc("QMS Document Category", self.category_name)
        self.assertEqual(cat.category_name, "Test Category")
        self.assertEqual(cat.description, "Test description")

    def test_update_category(self):
        """Test updating a QMS Document Category."""
        cat = frappe.get_doc("QMS Document Category", self.category_name)
        cat.description = "Updated description"
        cat.requires_periodic_review = 0
        cat.save()
        frappe.db.commit()
        updated = frappe.get_doc("QMS Document Category", self.category_name)
        self.assertEqual(updated.description, "Updated description")

    def test_category_name_unique(self):
        """Test that category name must be unique."""
        with self.assertRaises(frappe.DuplicateEntryError):
            dup_cat = frappe.get_doc({
                "doctype": "QMS Document Category",
                "category_name": "Test Category",
                "description": "Different"
            })
            dup_cat.insert()

    def test_delete_category(self):
        """Test deleting a QMS Document Category."""
        cat = frappe.get_doc("QMS Document Category", self.category_name)
        cat.delete()
        self.assertFalse(frappe.db.exists("QMS Document Category", self.category_name))

    def test_periodic_review_fields(self):
        """Test periodic review field defaults."""
        cat = frappe.get_doc("QMS Document Category", self.category_name)
        self.assertEqual(cat.requires_periodic_review, 1)
        self.assertEqual(cat.review_frequency_in_months, 12)
        self.assertEqual(cat.retention_period_in_years, 7)