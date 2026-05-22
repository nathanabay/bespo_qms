import frappe

def execute():
    for dt in ["Internal Document", "Incoming Document", "Outgoing Document"]:
        doc = frappe.get_doc("DocType", dt)
        dirty = False
        for field in doc.fields:
            if field.fieldname == "department":
                field.fieldtype = "Link"
                field.options = "QMS Department"
                dirty = True
            elif field.fieldname == "category":
                field.fieldtype = "Link"
                field.options = "QMS Document Category"
                dirty = True
            elif field.fieldname == "target_audience" and dt == "Outgoing Document":
                field.fieldtype = "Link"
                field.options = "QMS External Entity"
                dirty = True
            elif field.fieldname == "sender" and dt == "Incoming Document":
                field.fieldtype = "Link"
                field.options = "QMS External Entity"
                dirty = True
                
        if dirty:
            doc.save(ignore_permissions=True)
            print(f"Fixed {dt}.")

    frappe.db.commit()

if __name__ == "__main__":
    execute()
