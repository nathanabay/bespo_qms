app_name = "bespo_qms"
app_title = "Bespo QMS"
app_publisher = "BESPO"
app_description = "ISO 9001 Quality Management System — Document Control & Approval"
app_email = "NATHANAMARE@BESPO.ET"
app_license = "mit"
app_logo_url = "/assets/bespo_qms/images/bespo_qms_logo.png"

# Apps
# ------------------

# required_apps = []
fixtures = [
    {"dt": "Workflow", "filters": [["name", "in", ["Outgoing Document Approval", "Incoming Document Workflow", "Internal Document Workflow"]]]},
    {"dt": "Workflow State", "filters": [["name", "in", ["Draft", "Actioned", "Pending", "Approved", "Cancelled", "Dispatched"]]]},
    {"dt": "Workflow Action Master", "filters": [["name", "in", ["Complete", "Request Approval", "Approve", "Reject", "Cancel", "Submit for Approval", "Dispatch"]]]},
    {"dt": "Print Format", "filters": [["module", "=", "BESPO_QMS"]]},
    {"dt": "Role", "filters": [["name", "in", ["QMS User", "QMS Executive", "QMS Finance", "QMS Procurement", "QMS Engineering", "QMS HR"]]]},
    {"dt": "Notification", "filters": [["name", "=", "Outgoing Document Approved"]]},
    {"dt": "Client Script", "filters": [["module", "=", "BESPO_QMS"]]},
    {"dt": "Kanban Board", "filters": [["name", "in", ["Finance Approvals", "Procurement Approvals", "Engineering Approvals", "HR Approvals"]]]},
    {"dt": "Workspace", "filters": [["name", "=", "Bespo QMS"]]}
]

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "bespo_qms",
# 		"logo": "/assets/bespo_qms/logo.png",
# 		"title": "BESPO_QMS",
# 		"route": "/bespo_qms",
# 		"has_permission": "bespo_qms.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/bespo_qms/css/bespo_qms.css"
# app_include_js = "/assets/bespo_qms/js/bespo_qms.js"

# include js, css files in header of web template
# web_include_css = "/assets/bespo_qms/css/bespo_qms.css"
# web_include_js = "/assets/bespo_qms/js/bespo_qms.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "bespo_qms/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "bespo_qms/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "bespo_qms.utils.jinja_methods",
# 	"filters": "bespo_qms.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "bespo_qms.install.before_install"
# after_install = "bespo_qms.install.after_install"
after_install = [
    "bespo_qms.setup_workflows.setup_workflows",
    "bespo_qms.setup_notification.setup_email_notification",
    "bespo_qms.setup_sla_alerts.setup_sla_alerts",
    "bespo_qms.setup_print_format.setup_print_format",
]

# Uninstallation
# ------------

# before_uninstall = "bespo_qms.uninstall.before_uninstall"
# after_uninstall = "bespo_qms.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "bespo_qms.utils.before_app_install"
# after_app_install = "bespo_qms.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "bespo_qms.utils.before_app_uninstall"
# after_app_uninstall = "bespo_qms.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "bespo_qms.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events
# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

permission_query_conditions = {
    "Incoming Document": "bespo_qms.permissions.get_incoming_query",
    "Outgoing Document": "bespo_qms.permissions.get_outgoing_query",
    "Internal Document": "bespo_qms.permissions.get_internal_query"
}

has_permission = {
    "Incoming Document": "bespo_qms.permissions.has_qms_permission",
    "Outgoing Document": "bespo_qms.permissions.has_qms_permission",
    "Internal Document": "bespo_qms.permissions.has_qms_permission"
}


# Scheduled Tasks
# ---------------

scheduler_events = {
    "daily": [
        "bespo_qms.setup_sla_alerts.setup_sla_alerts"
    ],
}

# Testing
# -------

# before_tests = "bespo_qms.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "bespo_qms.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "bespo_qms.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["bespo_qms.utils.before_request"]
# after_request = ["bespo_qms.utils.after_request"]

# Job Events
# ----------
# before_job = ["bespo_qms.utils.before_job"]
# after_job = ["bespo_qms.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"bespo_qms.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
# ignore_translatable_strings_from = []

