def get_data():
    return [
        {
            "label": "QMS",
            "items": [
                {"type": "doctype", "name": "Incoming Document", "label": "Incoming Documents"},
                {"type": "doctype", "name": "Outgoing Document", "label": "Outgoing Documents"},
                {"type": "doctype", "name": "Internal Document", "label": "Internal Documents"},
                {"type": "separator"},
                {"type": "doctype", "name": "QMS Department", "label": "QMS Department"},
                {"type": "doctype", "name": "QMS Document Category", "label": "QMS Document Category"},
                {"type": "doctype", "name": "QMS External Entity", "label": "QMS External Entity"},
            ]
        }
    ]