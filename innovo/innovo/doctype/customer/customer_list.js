frappe.listview_settings['Customer'] = {
    add_fields: [
        "project",
        "status",
        "priority",
        "expected_start_date",
        "expected_end_date",
        "subject",
        "task_for"
    ],


    formatters: {
        priority: function (value) {
            if (!value) return '';

            // Use Frappe's standard indicator colors
            const customer_group_colors = {
                "Commercial": "red",
                "Government": "orange",
                "Urgent": "yellow",
                "Less Urgent": "blue"
            };

            const color = customer_group_colors[value] || 'grey';

            // Use Frappe's built-in indicator-pill classes
            return `<span class="indicator-pill ${color}">${__(value)}</span>`;
        },

        subject: function (value, _field, doc) {
            if (!value) return '';

            // Add project info if available
            let display = value;
            if (doc.customer) {
                display += ` <small class="text-muted">(${doc.project})</small>`;
            }

            return display;
        }
    }
};
