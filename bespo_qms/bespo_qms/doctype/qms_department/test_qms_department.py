# Copyright (c) 2026, BESPO and contributors
# For license information, please see license.txt

import frappe
from frappe.tests.utils import FrappeTestCase


class TestQMSDepartment(FrappeTestCase):
    """Tests for QMS Department DocType."""

    def setUp(self):
        """Set up test data."""
        frappe.set_user("Administrator")
        # Create a test department for use in tests
        self.test_department = frappe.get_doc({
            "doctype": "QMS Department",
            "department_name": "Test Department",
            "department_code": "TEST"
        }).insert()
        self.department_name = self.test_department.name

    def tearDown(self):
        """Clean up test data."""
        frappe.set_user("Administrator")
        # Delete the test department if it exists
        if frappe.db.exists("QMS Department", self.department_name):
            frappe.delete_doc("QMS Department", self.department_name, force=True)
        frappe.db.commit()

    def test_create_department(self):
        """Test creating a new QMS Department."""
        dept = frappe.get_doc({
            "doctype": "QMS Department",
            "department_name": "Quality Assurance",
            "department_code": "QA"
        })
        dept.insert()
        self.assertTrue(dept.name)
        self.assertEqual(dept.department_name, "Quality Assurance")
        self.assertEqual(dept.department_code, "QA")

    def test_read_department(self):
        """Test reading an existing QMS Department."""
        dept = frappe.get_doc("QMS Department", self.department_name)
        self.assertEqual(dept.department_name, "Test Department")
        self.assertEqual(dept.department_code, "TEST")

    def test_update_department(self):
        """Test updating a QMS Department."""
        dept = frappe.get_doc("QMS Department", self.department_name)
        dept.department_code = "UPD"
        dept.save()
        frappe.db.commit()
        updated = frappe.get_doc("QMS Department", self.department_name)
        self.assertEqual(updated.department_code, "UPD")

    def test_department_name_unique(self):
        """Test that department name must be unique."""
        with self.assertRaises(frappe.DuplicateEntryError):
            dup_dept = frappe.get_doc({
                "doctype": "QMS Department",
                "department_name": "Test Department",
                "department_code": "DIFF"
            })
            dup_dept.insert()

    def test_delete_department(self):
        """Test deleting a QMS Department."""
        dept = frappe.get_doc("QMS Department", self.department_name)
        dept.delete()
        self.assertFalse(frappe.db.exists("QMS Department", self.department_name))