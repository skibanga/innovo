// Copyright (c) 2024, Innovo and contributors
// For license information, please see license.txt

frappe.listview_settings['Prospect'] = {
	add_fields: [
		"prospect_name",
		"status",
		"prospect_type",
		"industry",
		"contact_name",
		"location"
	],

	filters: [["status", "in", "Open, Contacted"]],

	onload: function (listview) {
		// Add custom buttons for bulk operations
		listview.page.add_menu_item(__("Set as prospect"), function () {
			listview.call_for_selected_items("innovo.api.set_multiple_prospect_status", {
				status: "prospect"
			});
		});

		listview.page.add_menu_item(__("Set as Customer"), function () {
			listview.call_for_selected_items("innovo.api.set_multiple_prospect_status", {
				status: "Customer"
			});
		});
	},

	formatters: {
		prospect_type: function (value) {
			if (!value) return '';

			// Use Frappe's standard indicator colors for prospect types
			const type_colors = {
				"Import": "blue",      // Import operations - blue (calm, professional)
                "Export": "green",     // Export operations - green (success, growth)
                "Tendering": "purple", // Tendering process - purple (attention, active)
                "Sourcing": "pink", // Sourcing activities - pink (strategic, planning)
				"Innovo Insurance": "yellow"   // Sourcing activities - purple (strategic, planning)
			};

			const color = type_colors[value] || 'grey';

			// Use Frappe's built-in indicator-pill classes
			return `<span class="indicator-pill ${color}">${__(value)}</span>`;
		}
	}
};
			return '';
