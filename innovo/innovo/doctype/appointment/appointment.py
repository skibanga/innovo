# Copyright (c) 2025, Arnold Simony and contributors
# For license information, please see license.txt


import frappe
import datetime
from frappe.utils import get_datetime

def validate(doc, method=None):
    """Ensure duration is correct when saving via API/import/etc."""
    if doc.start_datetime and doc.end_datetime:
        start = get_datetime(doc.start_datetime)
        end = get_datetime(doc.end_datetime)
        if end < start:
            frappe.throw("End Time must be after Start Time.")
        minutes = int((end - start).total_seconds() // 60)
        doc.duration = minutes
# # import frappe
# from frappe.model.document import Document


# class Appointment(Document):
# 	pass
