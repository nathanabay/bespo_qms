import frappe

def update_client_script():
    frappe.set_user("Administrator")
    
    script_name = "Auto Populate Recipient on Outgoing Document"
    
    if frappe.db.exists("Client Script", script_name):
        doc = frappe.get_doc("Client Script", script_name)
        doc.script = """
frappe.ui.form.on('Outgoing Document', {
    // ── Customer ──────────────────────────────────────────────────────────────
    customer: function(frm) {
        if (!frm.doc.customer) return;
        frappe.call({
            method: 'frappe.client.get',
            args: { doctype: 'Customer', name: frm.doc.customer },
            callback: function(r) {
                if (!r.message) return;
                frm.set_value('recipient_name', r.message.customer_name || frm.doc.customer);
                // Try to fetch the primary contact email
                frappe.call({
                    method: 'frappe.client.get_list',
                    args: {
                        doctype: 'Dynamic Link',
                        filters: { link_doctype: 'Customer', link_name: frm.doc.customer, parenttype: 'Contact' },
                        parent: 'Contact',
                        fields: ['parent']
                    },
                    callback: function(res) {
                        if (!res.message || !res.message.length) return;
                        frappe.call({
                            method: 'frappe.client.get',
                            args: { doctype: 'Contact', name: res.message[0].parent },
                            callback: function(cr) {
                                if (!cr.message) return;
                                let c = cr.message;
                                frm.set_value('recipient_name', (c.first_name || '') + (c.last_name ? ' ' + c.last_name : ''));
                                if (c.email_ids && c.email_ids.length)
                                    frm.set_value('recipient_email', c.email_ids[0].email_id);
                            }
                        });
                    }
                });
            }
        });
    },

    // ── Opportunity ───────────────────────────────────────────────────────────
    opportunity: function(frm) {
        if (!frm.doc.opportunity) return;
        frappe.call({
            method: 'bespo_qms.BESPO_QMS.doctype.outgoing_document.outgoing_document.get_opportunity_details',
            args: { opportunity: frm.doc.opportunity },
            callback: function(r) {
                if (!r.message) return;
                let d = r.message;
                if (d.opportunity_amount)  frm.set_value('opportunity_value',      d.opportunity_amount);
                if (d.expected_closing)    frm.set_value('opportunity_close_date', d.expected_closing);
                if (d.customer_name && !frm.doc.recipient_name)
                    frm.set_value('recipient_name', d.customer_name);
                frm.set_value('context_notes',
                    'Linked Opportunity: ' + frm.doc.opportunity +
                    (d.contact_display ? ' · Contact: ' + d.contact_display : '')
                );
            }
        });
    },

    // ── Project ───────────────────────────────────────────────────────────────
    project: function(frm) {
        if (!frm.doc.project) return;
        frappe.call({
            method: 'bespo_qms.BESPO_QMS.doctype.outgoing_document.outgoing_document.get_project_details',
            args: { project: frm.doc.project },
            callback: function(r) {
                if (!r.message) return;
                let d = r.message;
                if (d.expected_end_date) frm.set_value('project_deadline', d.expected_end_date);
                let notes = 'Project: ' + (d.project_name || frm.doc.project);
                if (d.expected_start_date) notes += ' | Start: ' + d.expected_start_date;
                if (d.percent_complete)    notes += ' | Progress: ' + d.percent_complete + '%';
                frm.set_value('context_notes', notes);
            }
        });
    }
});
"""
        doc.save(ignore_permissions=True)
        print(f"Client Script '{script_name}' updated successfully.")
    else:
        print(f"Client Script '{script_name}' not found. Please create it first.")

    frappe.db.commit()

if __name__ == "__main__":
    update_client_script()
