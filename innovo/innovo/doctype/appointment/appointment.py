# Copyright (c) 2025, Arnold Simony and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import get_datetime, time_diff_in_seconds


class Appointment(Document):
	def validate(self):
		"""Validate appointment data"""
		self.calculate_duration()
		self.validate_innovo_office_booking()

	def calculate_duration(self):
		"""Calculate duration in minutes between start and end datetime"""
		if self.start_datetime and self.end_datetime:
			start_dt = get_datetime(self.start_datetime)
			end_dt = get_datetime(self.end_datetime)

			# Validate that end time is after start time
			if end_dt <= start_dt:
				frappe.throw("End datetime must be after start datetime")

			# Calculate duration in seconds and convert to minutes
			duration_seconds = time_diff_in_seconds(end_dt, start_dt)
			self.duration = duration_seconds / 60  # Convert to minutes

	def validate_innovo_office_booking(self):
		"""Prevent double booking for Innovo Office location"""
		if self.location_type != "Innovo Office":
			return

		if not self.start_datetime or not self.end_datetime:
			return

		# Check for overlapping appointments at Innovo Office
		overlapping_appointments = frappe.db.sql("""
			SELECT name, title, start_datetime, end_datetime
			FROM `tabAppointment`
			WHERE location_type = 'Innovo Office'
			AND name != %(current_appointment)s
			AND status NOT IN ('Canceled', 'No-show')
			AND (
				(start_datetime < %(end_datetime)s AND end_datetime > %(start_datetime)s)
			)
		""", {
			'current_appointment': self.name or '',
			'start_datetime': self.start_datetime,
			'end_datetime': self.end_datetime
		}, as_dict=True)

		if overlapping_appointments:
			conflict = overlapping_appointments[0]
			conflict_start = frappe.utils.format_datetime(conflict.start_datetime)
			conflict_end = frappe.utils.format_datetime(conflict.end_datetime)

			frappe.throw(
				f"Innovo Office is already booked during this time slot.<br><br>"
				f"<strong>Conflicting Appointment:</strong><br>"
				f"• Title: {conflict.title}<br>"
				f"• Time: {conflict_start} to {conflict_end}<br><br>"
				f"Please choose a different time slot or location.",
				title="Double Booking Detected"
			)

