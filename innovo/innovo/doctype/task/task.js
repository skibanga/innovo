// Copyright (c) 2025, Arnold Simony and contributors
// For license information, please see license.txt

frappe.ui.form.on("Task", {
    refresh(frm) {
        // Add custom buttons for task management
        if (!frm.doc.__islocal && frm.doc.project && frm.doc.task_for === 'Project') {
            frm.add_custom_button(__('View Project'), function () {
                frappe.set_route('Form', 'Project', frm.doc.project);
            });

            frm.add_custom_button(__('Add to Project'), function () {
                frappe.call({
                    method: 'innovo.api.add_task_to_project',
                    args: {
                        task_name: frm.doc.name,
                        project_name: frm.doc.project
                    },
                    callback: function (r) {
                        if (r.message && r.message.success) {
                            frappe.msgprint(r.message.message);
                        } else if (r.message && !r.message.success) {
                            frappe.msgprint(r.message.message, __('Info'));
                        }
                    }
                });
            });
        }

        // Show project information if task is linked to a project
        if (frm.doc.project && frm.doc.task_for === 'Project') {
            frappe.db.get_doc('Project', frm.doc.project).then(project_doc => {
                frm.dashboard.set_headline_alert(
                    `This task belongs to project: ${project_doc.project_title} (${project_doc.status})`,
                    'blue'
                );
            });
        }

        // Keep original status indicators only - no custom modifications
    },

    task_for(frm) {
        // Clear project field when task_for changes to Strategic Goal
        if (frm.doc.task_for === 'Strategic Goal') {
            frm.set_value('project', '');
            frm.set_value('project_title', '');
        }
        // Clear strategic_goal field when task_for changes to Project
        else if (frm.doc.task_for === 'Project') {
            frm.set_value('strategic_goal', '');
        }
    },

    project(frm) {
        // Auto-fetch project title when project is selected
        if (frm.doc.project) {
            frappe.db.get_value('Project', frm.doc.project, 'project_title').then(r => {
                if (r.message && r.message.project_title) {
                    frm.set_value('project_title', r.message.project_title);
                }
            });
        } else {
            frm.set_value('project_title', '');
        }
    },

    status(frm) {
        // Show confirmation when marking task as completed
        if (frm.doc.status === 'Completed' && frm.doc.project) {
            frappe.msgprint({
                title: __('Task Completed'),
                message: __('This task has been marked as completed. The project progress will be automatically updated.'),
                indicator: 'green'
            });
        }
    },

    before_save(frm) {
        // Validate dates
        if (frm.doc.expected_start_date && frm.doc.expected_end_date) {
            if (frm.doc.expected_start_date > frm.doc.expected_end_date) {
                frappe.throw(__('Expected Start Date cannot be greater than Expected End Date'));
            }
        }

        // Auto-set task_for if project is selected
        if (frm.doc.project && !frm.doc.task_for) {
            frm.set_value('task_for', 'Project');
        }
    }
});
