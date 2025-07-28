# Copyright (c) 2025, Arnold Simony and contributors
# For license information, please see license.txt

import frappe


# def execute(filters=None):
# 	columns, data = [], []
# 	return columns, data
# Completed Projects Script Report

def execute(filters=None):
    columns = [
        {"label": "Project Title", "fieldname": "project_title", "fieldtype": "Data", "width": 300},
        {"label": "Category", "fieldname": "category", "fieldtype": "Select", "width": 120},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 100},
        {"label": "Project Lead", "fieldname": "project_lead", "fieldtype": "Link", "options": "User", "width": 250},
        {"label": "Lead Name", "fieldname": "lead_name", "fieldtype": "Data", "width": 180},
        {"label": "Client", "fieldname": "client", "fieldtype": "Link", "options": "Customer", "width": 150},
    ]

    # Adjusted for commonly used fieldnames
    data = frappe.db.get_all(
        "Project",
        filters={"status": "Completed"},
        fields=["name", "project_title", "category", "status", "project_lead", "lead_name", "client"]
    )

    if not data:
        # Debug message if nothing is returned
        frappe.msgprint("⚠️ No data returned. Please check: 1) Project has status='Completed', 2) Fields exist.")

    return columns, data

