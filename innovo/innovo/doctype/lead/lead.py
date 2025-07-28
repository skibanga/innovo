# Copyright (c) 2025, Arnold Simony and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import comma_and, get_link_to_form, has_gravatar, validate_email_address
from innovo.innovo.doctype.prospect.prospect import Prospect
from innovo.innovo.doctype.prospect.prospect import update_prospect
from frappe.model.document import Document


class Lead(Document):
	pass
	# def validate(self):
	# 	self.set_full_name()
	# 	self.set_lead_name()
	# 	self.set_title()
	# 	self.set_status()
	# 	self.check_email_id_is_unique()
	# 	self.validate_email_id()

	# def on_update(self):
	# 	self.update_prospect()

	# def set_full_name(self):
	# 	if self.first_name:
	# 		self.lead_name = " ".join(
	# 			filter(None, [self.salutation, self.first_name, self.middle_name, self.last_name])
	# 		)

	# def set_lead_name(self):
	# 	if not self.lead_name:
	# 		# Check for leads being created through data import
	# 		if not self.company_name and not self.email_id and not self.flags.ignore_mandatory:
	# 			frappe.throw(_("A Lead requires either a person's name or an organization's name"))
	# 		elif self.company_name:
	# 			self.lead_name = self.company_name
	# 		else:
	# 			self.lead_name = self.email_id.split("@")[0]

	# def set_title(self):
	# 	self.title = self.company_name or self.lead_name

	# def check_email_id_is_unique(self):
	# 	if self.email_id:
	# 		# validate email is unique
	# 		if not frappe.db.get_single_value("CRM Settings", "allow_lead_duplication_based_on_emails"):
	# 			duplicate_leads = frappe.get_all(
	# 				"Lead", filters={"email_id": self.email_id, "name": ["!=", self.name]}
	# 			)
	# 			duplicate_leads = [
	# 				frappe.bold(get_link_to_form("Lead", lead.name)) for lead in duplicate_leads
	# 			]

	# 			if duplicate_leads:
	# 				frappe.throw(
	# 					_("Email Address must be unique, it is already used in {0}").format(
	# 						comma_and(duplicate_leads)
	# 					),
	# 					frappe.DuplicateEntryError,
	# 				)

	# def validate_email_id(self):
	# 	if self.email_id:
	# 		if not self.flags.ignore_email_validation:
	# 			validate_email_address(self.email_id, throw=True)

	# 		if self.email_id == self.lead_owner:
	# 			frappe.throw(_("Lead Owner cannot be same as the Lead Email Address"))

	# 		if self.is_new() or not self.image:
	# 			self.image = has_gravatar(self.email_id)


