// Copyright (c) 2025, Arnold Simony and contributors
// For license information, please see license.txt

frappe.listview_settings['Customer'] = {
	add_fields: [
		"customer_name",
		"customer_group",
		"customer_type",
		"industry"

	],

	filters: [["customer_status", "in", "Active, Potential"]],

	onload: function (listview) {
		// Add custom buttons for bulk operations
		listview.page.add_menu_item(__("Set as Active"), function () {
			listview.call_for_selected_items("innovo.api.set_multiple_customer_status", {
				customer_status: "Active"
			});
		});

		listview.page.add_menu_item(__("Set as Inactive"), function () {
			listview.call_for_selected_items("innovo.api.set_multiple_customer_status", {
				customer_status: "Inactive"
			});
		});

		listview.page.add_menu_item(__("Set as Potential"), function () {
			listview.call_for_selected_items("innovo.api.set_multiple_customer_status", {
				customer_status: "Potential"
			});
		});
	},

	formatters: {
		customer_type: function (value) {
			if (!value) return '';

			// Use Frappe's standard indicator colors for customer types
			const type_colors = {
				"Import": "blue",      // Import operations - blue (calm, professional)
				"Export": "green",     // Export operations - green (success, growth)
				"Tendering": "purple", // Tendering process - purple (attention, active)
				"Sourcing": "pink", // Sourcing activities - pink (strategic, planning)
				"Innovo Insurance": "yellow"   // Sourcing activities - yellow (strategic, planning)
			};
			const color = type_colors[value] || 'grey';

			// Use Frappe's built-in indicator-pill classes
			return `<span class="indicator-pill ${color}">${__(value)}</span>`;
		}
	}
};
