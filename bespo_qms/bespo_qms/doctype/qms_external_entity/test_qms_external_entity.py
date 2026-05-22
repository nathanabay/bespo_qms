# Copyright (c) 2026, BESPO and contributors
# For license information, please see license.txt

import frappe
from frappe.tests.utils import FrappeTestCase


class TestQMSExternalEntity(FrappeTestCase):
    """Tests for QMS External Entity DocType."""

    def setUp(self):
        """Set up test data."""
        frappe.set_user("Administrator")
        self.test_entity = frappe.get_doc({
            "doctype": "QMS External Entity",
            "entity_name": "Test Entity",
            "entity_type": "Client",
            "primary_contact_person": "John Doe",
            "contact_email": "john@test.com",
            "primary_phone": "+1234567890"
        }).insert()
        self.entity_name = self.test_entity.name

    def tearDown(self):
        """Clean up test data."""
        frappe.set_user("Administrator")
        if frappe.db.exists("QMS External Entity", self.entity_name):
            frappe.delete_doc("QMS External Entity", self.entity_name, force=True)
        frappe.db.commit()

    def test_create_entity(self):
        """Test creating a new QMS External Entity."""
        entity = frappe.get_doc({
            "doctype": "QMS External Entity",
            "entity_name": "Acme Corp",
            "entity_type": "Supplier",
            "primary_contact_person": "Jane Smith",
            "contact_email": "jane@acme.com"
        })
        entity.insert()
        self.assertTrue(entity.name)
        self.assertEqual(entity.entity_name, "Acme Corp")
        self.assertEqual(entity.entity_type, "Supplier")

    def test_read_entity(self):
        """Test reading an existing QMS External Entity."""
        entity = frappe.get_doc("QMS External Entity", self.entity_name)
        self.assertEqual(entity.entity_name, "Test Entity")
        self.assertEqual(entity.entity_type, "Client")
        self.assertEqual(entity.contact_email, "john@test.com")

    def test_update_entity(self):
        """Test updating a QMS External Entity."""
        entity = frappe.get_doc("QMS External Entity", self.entity_name)
        entity.entity_type = "Supplier"
        entity.primary_phone = "+9876543210"
        entity.save()
        frappe.db.commit()
        updated = frappe.get_doc("QMS External Entity", self.entity_name)
        self.assertEqual(updated.entity_type, "Supplier")
        self.assertEqual(updated.primary_phone, "+9876543210")

    def test_entity_name_unique(self):
        """Test that entity name must be unique."""
        with self.assertRaises(frappe.DuplicateEntryError):
            dup_entity = frappe.get_doc({
                "doctype": "QMS External Entity",
                "entity_name": "Test Entity",
                "entity_type": "Government"
            })
            dup_entity.insert()

    def test_delete_entity(self):
        """Test deleting a QMS External Entity."""
        entity = frappe.get_doc("QMS External Entity", self.entity_name)
        entity.delete()
        self.assertFalse(frappe.db.exists("QMS External Entity", self.entity_name))

    def test_entity_types(self):
        """Test valid entity types."""
        for entity_type in ["Client", "Supplier", "Government", "Regulator", "Auditor", "Other"]:
            entity = frappe.get_doc({
                "doctype": "QMS External Entity",
                "entity_name": f"Entity {entity_type}",
                "entity_type": entity_type
            })
            entity.insert()
            self.assertEqual(entity.entity_type, entity_type)
            frappe.delete_doc("QMS External Entity", entity.name, force=True)