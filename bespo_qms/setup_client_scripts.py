import frappe
import json

def create_client_scripts():
    frappe.set_user("Administrator")
    
    script_name = "QMS Dynamic Categories"
    
    doctypes = ["Incoming Document", "Outgoing Document", "Internal Document"]
    
    # Define exact category lists grouped by doctype and department, matching their strict database schemas!
    categories = {
        "Incoming Document": {
            "Finance": ["", "Tax Notices", "Bank Notices", "Letter of Credit (L/C) Advices", "Guarantee Advices"],
            "Procurement": ["", "Supplier Quotations & Bids", "Shipping & Freight Notices", "Supplier Non-Conformance Notifications"],
            "Engineering": ["", "Tender Invitations / Requests for Proposal (RFPs)", "Site / Architect Instructions", "Approval Status Letters", "Notices of Award / Notices to Proceed"],
            "HR": ["", "Other"],
            "Other": ["", "Municipal & Authority Directives", "Customs & Import Directives", "Other"]
        },
        "Outgoing Document": {
            "Finance": ["", "Bank Letters", "Payment Requisitions & Invoicing", "Tax Compliance Declarations"],
            "Procurement": ["", "Supplier Corrective Action Requests (SCAR)", "Purchase Orders (POs)"],
            "Engineering": ["", "Tender Submissions", "Requests for Extension of Time (EOT)", "Prequalification Submissions", "Technical Submittals", "Requests for Information (RFIs)", "Inspection Requests", "Project Handover Letters"],
            "HR": ["", "Other"],
            "Other": ["", "Other", "Letter", "Invoice", "Report", "Proposal", "Quote"]
        },
        "Internal Document": {
            "Finance": ["", "Inter-Departmental Memos"],
            "Procurement": ["", "Inter-Departmental Memos"],
            "Engineering": ["", "Site Progress Reports", "Equipment Maintenance Schedules", "Inter-Departmental Memos"],
            "HR": ["", "Policy Announcements", "Disciplinary & Corrective Notices"],
            "Other": ["", "Corrective and Preventative Action (CAPA) Directives", "Internal Audit Reports & Notices", "Document Change Requests (DCR)", "Management Review Memos", "Other"]
        }
    }
    
    for dt in doctypes:
        dt_cats = categories[dt]
        
        acknowledge_button_js = ""
        if dt == "Internal Document":
            acknowledge_button_js = """

    // Acknowledge Policy button — only visible to logged-in QMS Users
    if (frm.doc.status === 'Approved' && !frm.is_new()) {
        let already_acknowledged = (frm.doc.acknowledgements || []).some(
            r => r.user === frappe.session.user && r.status === 'Acknowledged'
        );
        if (!already_acknowledged) {
            frm.add_custom_button(__('Acknowledge Policy'), function() {
                frappe.call({
                    method: 'bespo_qms.BESPO_QMS.doctype.internal_document.internal_document.acknowledge_policy',
                    args: { docname: frm.doc.name },
                    callback: function(r) {
                        frappe.show_alert({ message: 'Policy acknowledged!', indicator: 'green' }, 3);
                        frm.reload_doc();
                    }
                });
            }, __('Actions')).addClass('btn-success');
        } else {
            frm.add_custom_button(__('✓ Acknowledged'), function() {}, __('Actions')).prop('disabled', true);
        }
    }"""
        
        js_code = f"""
frappe.ui.form.on("{dt}", {{
    department: function(frm) {{
        set_category_options_{dt.replace(' ', '_')}(frm);
    }},
    refresh: function(frm) {{
        set_category_options_{dt.replace(' ', '_')}(frm);
        {acknowledge_button_js}
    }}
}});

function set_category_options_{dt.replace(' ', '_')}(frm) {{
    let options = ["", "Other"];
    
    if (frm.doc.department === "Finance") {{
        options = {json.dumps(dt_cats['Finance'])};
    }} else if (frm.doc.department === "Procurement") {{
        options = {json.dumps(dt_cats['Procurement'])};
    }} else if (frm.doc.department === "Engineering") {{
        options = {json.dumps(dt_cats['Engineering'])};
    }} else if (frm.doc.department === "HR") {{
        options = {json.dumps(dt_cats['HR'])};
    }} else if (frm.doc.department === "Other") {{
        options = {json.dumps(dt_cats['Other'])};
    }}
    
    frm.set_df_property("category", "options", options);
}}
"""
        s_name = f"{script_name} - {dt}"
        if frappe.db.exists("Client Script", s_name):
            doc = frappe.get_doc("Client Script", s_name)
            frappe.db.set_value("Client Script", s_name, "script", js_code, update_modified=True)
            print(f"Updated script for {dt}")
        else:
            frappe.get_doc({
                "doctype": "Client Script",
                "name": s_name,
                "dt": dt,
                "module": "BESPO_QMS",
                "script": js_code,
                "enabled": 1
            }).insert(ignore_permissions=True)
            print(f"Created script for {dt}")
            
    frappe.db.commit()

if __name__ == "__main__":
    create_client_scripts()
