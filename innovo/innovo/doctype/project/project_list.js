// Copyright (c) 2025, Arnold Simony and contributors
// For license information, please see license.txt

frappe.listview_settings['Project'] = {
    add_fields: [
        "project_title",
        "category",
        "status",
        "progress_rate",
        "client",
        "project_lead",
        "kickoff_date",
        "due_date"
    ],

    filters: [["status", "=", "Open"]],

    onload: function (listview) {
        // Add custom buttons for bulk operations
        listview.page.add_menu_item(__("Set as Open"), function () {
            listview.call_for_selected_items("innovo.api.set_multiple_project_status", {
                status: "Open"
            });
        });

        listview.page.add_menu_item(__("Set as Progress"), function () {
            listview.call_for_selected_items("innovo.api.set_multiple_project_status", {
                status: "Progress"
            });
        });

        listview.page.add_menu_item(__("Set as Completed"), function () {
            listview.call_for_selected_items("innovo.api.set_multiple_project_status", {
                status: "Completed"
            });
        });
    },

    formatters: {
        category: function (value) {
            if (!value) return '';

            // Use Frappe's standard indicator colors for categories
            const category_colors = {
                "Import": "blue",      // Import operations - blue (calm, professional)
                "Export": "green",     // Export operations - green (success, growth)
                "Tendering": "purple", // Tendering process - purple (attention, active)
                "Sourcing": "pink", // Sourcing activities - pink (strategic, planning)
				"Innovo Insurance": "yellow"   // Sourcing activities - yellow (strategic, planning)
            };

            const color = category_colors[value] || 'grey';

            // Use Frappe's built-in indicator-pill classes
            return `<span class="indicator-pill ${color}">${__(value)}</span>`;
        },

        progress_rate: function (value) {
            if (value == null || value === '') return '';

            // Format progress as percentage with visual indicator
            const percentage = parseFloat(value) || 0;
            let color = 'blue';

            if (percentage >= 100) color = 'green';
            else if (percentage >= 75) color = 'light-blue';
            else if (percentage >= 50) color = 'orange';
            else if (percentage >= 25) color = 'yellow';
            else color = 'red';

            return `<span class="indicator-pill ${color}">${percentage.toFixed(0)}%</span>`;
        },

        project_title: function (value, _field, doc) {
            if (!value) return '';

            // Add client info if available
            let display = value;
            if (doc.progress_rate1) {
                display += `(${doc.progress_rate1})`;
            }

            return display;
        }
    }
};
