// Copyright (c) 2025, Arnold Simony and contributors
// For license information, please see license.txt

frappe.listview_settings['Task'] = {
    add_fields: [
        "project",
        "status",
        "priority",
        "expected_start_date",
        "expected_end_date",
        "subject",
        "task_for"
    ],

    filters: [["status", "=", "Open"]],

    onload: function (listview) {
        // Add custom buttons for bulk operations
        listview.page.add_menu_item(__("Set as Open"), function () {
            listview.call_for_selected_items("innovo.api.set_multiple_task_status", {
                status: "Open"
            });
        });

        listview.page.add_menu_item(__("Set as Working"), function () {
            listview.call_for_selected_items("innovo.api.set_multiple_task_status", {
                status: "Working"
            });
        });

        listview.page.add_menu_item(__("Set as Completed"), function () {
            listview.call_for_selected_items("innovo.api.set_multiple_task_status", {
                status: "Completed"
            });
        });
    },

    formatters: {
        priority: function (value) {
            if (!value) return '';

            // Use Frappe's standard indicator colors
            const priority_colors = {
                "Super Important": "red",
                "Important": "orange",
                "Urgent": "yellow",
                "Less Urgent": "blue"
            };

            const color = priority_colors[value] || 'grey';

            // Use Frappe's built-in indicator-pill classes
            return `<span class="indicator-pill ${color}">${__(value)}</span>`;
        },

        subject: function (value, _field, doc) {
            if (!value) return '';

            // Add project info if available
            let display = value;
            if (doc.project) {
                display += ` <small class="text-muted">(${doc.project})</small>`;
            }

            return display;
        }
    }
};
