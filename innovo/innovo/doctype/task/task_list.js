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
    
    onload: function(listview) {
        // Add custom buttons for bulk operations
        listview.page.add_menu_item(__("Set as Open"), function() {
            listview.call_for_selected_items("innovo.api.set_multiple_task_status", {
                status: "Open"
            });
        });

        listview.page.add_menu_item(__("Set as Working"), function() {
            listview.call_for_selected_items("innovo.api.set_multiple_task_status", {
                status: "Working"
            });
        });

        listview.page.add_menu_item(__("Set as Completed"), function() {
            listview.call_for_selected_items("innovo.api.set_multiple_task_status", {
                status: "Completed"
            });
        });
    },

    get_indicator: function(doc) {
        // Priority indicators with colors
        const priority_colors = {
            "Super Important": "red",
            "Important": "orange", 
            "Urgent": "yellow",
            "Less Urgent": "blue"
        };

        // Status indicators (fallback)
        const status_colors = {
            "Open": "cyan",
            "Working": "blue",
            "Pending Review": "orange",
            "Overdue": "red",
            "Completed": "green",
            "Cancelled": "grey"
        };

        // Priority takes precedence for indicator
        if (doc.priority && priority_colors[doc.priority]) {
            return [__(doc.priority), priority_colors[doc.priority], "priority,=," + doc.priority];
        }
        
        // Fallback to status indicator
        if (doc.status && status_colors[doc.status]) {
            return [__(doc.status), status_colors[doc.status], "status,=," + doc.status];
        }

        return [__("Open"), "grey", "status,=,Open"];
    },

    formatters: {
        priority: function(value) {
            if (!value) return '';
            
            const priority_colors = {
                "Super Important": "red",
                "Important": "orange",
                "Urgent": "yellow", 
                "Less Urgent": "blue"
            };

            const color = priority_colors[value] || 'grey';
            
            return `<span class="indicator-pill ${color}">${__(value)}</span>`;
        },

        status: function(value) {
            if (!value) return '';
            
            const status_colors = {
                "Open": "cyan",
                "Working": "blue", 
                "Pending Review": "orange",
                "Overdue": "red",
                "Completed": "green",
                "Cancelled": "grey"
            };

            const color = status_colors[value] || 'grey';
            
            return `<span class="indicator-pill ${color}">${__(value)}</span>`;
        },

        subject: function(value, field, doc) {
            if (!value) return '';
            
            // Add project info if available
            let display = value;
            if (doc.project) {
                display += ` <small class="text-muted">(${doc.project})</small>`;
            }
            
            return display;
        }
    },

    refresh: function(listview) {
        // Add custom styling for priority indicators
        if (!$('head').find('#task-priority-styles').length) {
            $('head').append(`
                <style id="task-priority-styles">
                    .indicator-pill {
                        display: inline-block;
                        padding: 2px 8px;
                        border-radius: 12px;
                        font-size: 11px;
                        font-weight: 500;
                        text-transform: uppercase;
                        letter-spacing: 0.5px;
                    }
                    
                    .indicator-pill.red {
                        background-color: #ff5858;
                        color: white;
                    }
                    
                    .indicator-pill.orange {
                        background-color: #ff9f43;
                        color: white;
                    }
                    
                    .indicator-pill.yellow {
                        background-color: #feca57;
                        color: #333;
                    }
                    
                    .indicator-pill.blue {
                        background-color: #3742fa;
                        color: white;
                    }
                    
                    .indicator-pill.cyan {
                        background-color: #00d2d3;
                        color: white;
                    }
                    
                    .indicator-pill.green {
                        background-color: #5f27cd;
                        color: white;
                    }
                    
                    .indicator-pill.grey {
                        background-color: #747d8c;
                        color: white;
                    }
                </style>
            `);
        }
    }
};
