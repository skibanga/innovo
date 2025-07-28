// Copyright (c) 2025, Arnold Simony and contributors
// For license information, please see license.txt

frappe.ui.form.on("Project", {
    refresh(frm) {
        // Add custom buttons for project management
        if (!frm.doc.__islocal) {
            frm.add_custom_button(__('Refresh Project Data'), function () {
                frm.call('refresh_project_data').then(() => {
                    frm.reload_doc();
                });
            });

            frm.add_custom_button(__('Get Project Summary'), function () {
                // Use API call instead of doc method as fallback
                frappe.call({
                    method: 'innovo.api.get_project_tasks_summary',
                    args: {
                        project_name: frm.doc.name
                    },
                    callback: function (r) {
                        if (r.message && !r.message.error) {
                            let summary = r.message;
                            let msg = `
								<h4>Project Summary</h4>
								<p><strong>Status:</strong> ${summary.project_status}</p>
								<p><strong>Progress:</strong> ${summary.progress_rate.toFixed(1)}%</p>
								<p><strong>Total Tasks:</strong> ${summary.total_tasks}</p>
								<p><strong>Completed Tasks:</strong> ${summary.completed_tasks}</p>
							`;
                            frappe.msgprint(msg, __('Project Summary'));
                        } else {
                            frappe.msgprint(__('Error getting project summary'), __('Error'));
                        }
                    }
                });
            });

        }

        // Update progress indicator
        if (frm.doc.progress_rate !== undefined) {
            frm.dashboard.add_progress(__('Project Progress'), frm.doc.progress_rate, __('% Complete'));
        }

        // Show task statistics
        if (!frm.doc.__islocal) {
            frm.call('get_project_summary').then(r => {
                if (r.message) {
                    let summary = r.message;
                    frm.dashboard.set_headline_alert(
                        `${summary.completed_tasks}/${summary.total_tasks} tasks completed`,
                        summary.completed_tasks === summary.total_tasks ? 'green' : 'blue'
                    );
                }
            });
        }
    },

    status(frm) {
        // Auto-set completed date when status is set to Completed
        if (frm.doc.status === 'Completed' && !frm.doc.completed_date) {
            frm.set_value('completed_date', frappe.datetime.get_today());
        }
    },

    project_lead(frm) {
        // Auto-fetch lead name when project lead is selected
        if (frm.doc.project_lead) {
            frappe.db.get_value('User', frm.doc.project_lead, 'full_name').then(r => {
                if (r.message && r.message.full_name) {
                    frm.set_value('lead_name', r.message.full_name);
                }
            });
        }
    }
});

// Child table events for Task Details
frappe.ui.form.on("Task Details", {
    task(frm, cdt, cdn) {
        // Auto-fetch task details when task is selected
        let row = locals[cdt][cdn];
        if (row.task) {
            frappe.db.get_doc('Task', row.task).then(task_doc => {
                frappe.model.set_value(cdt, cdn, 'expected_to_start', task_doc.expected_start_date);
                frappe.model.set_value(cdt, cdn, 'expected_to_end', task_doc.expected_end_date);
                frappe.model.set_value(cdt, cdn, 'description', task_doc.task_description || task_doc.subject);
            });
        }
    },

    assigned_to(frm, cdt, cdn) {
        // Auto-fetch team member name when assigned_to is selected
        let row = locals[cdt][cdn];
        if (row.assigned_to) {
            frappe.db.get_value('User', row.assigned_to, 'full_name').then(r => {
                if (r.message && r.message.full_name) {
                    frappe.model.set_value(cdt, cdn, 'team_name', r.message.full_name);
                }
            });
        }
    }
});
