import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def create_internal_document():
    if not frappe.db.exists("DocType", "Internal Document"):
        doc = frappe.new_doc("DocType")
        doc.name = "Internal Document"
        doc.module = "BESPO_QMS"
        doc.custom = 0
        doc.is_submittable = 1
        doc.autoname = "naming_series:"
        doc.naming_rule = 'By "Naming Series" field'
        
        fields = [
            {"fieldname": "document_info_section", "fieldtype": "Section Break", "label": "Document Information"},
            {"fieldname": "naming_series", "fieldtype": "Select", "label": "Series", "options": "QMS-INT-.YYYY.-.#####", "reqd": 1, "default": "QMS-INT-.YYYY.-.#####"},
            {"fieldname": "subject", "fieldtype": "Data", "label": "Subject", "reqd": 1},
            {
                "fieldname": "category",
                "fieldtype": "Select",
                "label": "Category",
                "options": "\nCorrective and Preventative Action (CAPA) Directives\nInternal Audit Reports & Notices\nDocument Change Requests (DCR)\nManagement Review Memos\nInter-Departmental Memos\nSite Progress Reports\nEquipment Maintenance Schedules\nPolicy Announcements\nDisciplinary & Corrective Notices\nOther",
                "reqd": 1
            },
            {"fieldname": "status", "fieldtype": "Select", "label": "Status", "options": "Draft\nPending\nApproved\nCancelled", "default": "Draft", "read_only": 1},
            {"fieldname": "cb1", "fieldtype": "Column Break"},
            {"fieldname": "document_date", "fieldtype": "Date", "label": "Document Date", "default": "Today", "reqd": 1},
            {"fieldname": "originating_department", "fieldtype": "Data", "label": "Originating Department"},
            {"fieldname": "target_audience", "fieldtype": "Data", "label": "Target Audience / Department"},
            
            {"fieldname": "content_section", "fieldtype": "Section Break", "label": "Document Content"},
            {"fieldname": "content", "fieldtype": "Text Editor", "label": "Content", "reqd": 1},
            {"fieldname": "attachment", "fieldtype": "Attach", "label": "Attachment"},
            
            {"fieldname": "amendment_reason", "fieldtype": "Data", "label": "Amendment Reason", "depends_on": "eval:doc.amended_from", "mandatory_depends_on": "eval:doc.amended_from", "reqd": 0},
            {"fieldname": "amended_from", "fieldtype": "Link", "label": "Amended From", "options": "Internal Document", "read_only": 1, "no_copy": 1, "print_hide": 1},
            {"fieldname": "approved_by", "fieldtype": "Data", "label": "Approved By", "read_only": 1}
        ]
        
        for f in fields:
            doc.append("fields", f)
            
        doc.append("permissions", {
            "role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1, "submit": 1, "cancel": 1, "amend": 1
        })
        doc.append("permissions", {
            "role": "QMS User", "read": 1, "write": 1, "create": 1
        })
        doc.append("permissions", {
            "role": "QMS Executive", "read": 1, "write": 1, "create": 1, "submit": 1, "cancel": 1, "amend": 1
        })
        
        doc.insert(ignore_permissions=True)
        frappe.db.commit()
        print("Internal Document DocType created successfully.")
    else:
        print("Internal Document DocType already exists. Skipping creation.")

if __name__ == "__main__":
    create_internal_document()
