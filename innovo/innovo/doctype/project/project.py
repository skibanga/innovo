# Copyright (c) 2025, Arnold Simony and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Project(Document):
    def validate(self):
        """Validate project data"""
        self.update_progress_rate()

    def on_update(self):
        """Handle project updates"""
        # Update task assignments when project team changes
        if self.has_value_changed("project_team"):
            self.sync_task_assignments()

    def update_progress_rate(self):
        """Calculate and update project progress based on completed tasks"""
        if not self.name:
            return

        # Get all tasks for this project
        project_tasks = frappe.get_all(
            "Task",
            filters={"project": self.name, "task_for": "Project"},
            fields=["name", "status"],
        )

        if not project_tasks:
            self.progress_rate = 0
            return

        # Calculate progress
        completed_tasks = [task for task in project_tasks if task.status == "Completed"]
        total_tasks = len(project_tasks)
        completed_count = len(completed_tasks)

        self.progress_rate = (
            (completed_count / total_tasks) * 100 if total_tasks > 0 else 0
        )

        # Auto-update status based on progress
        if completed_count == total_tasks and total_tasks > 0:
            self.status = "Completed"
            if not self.completed_date:
                self.completed_date = frappe.utils.today()
        elif completed_count > 0:
            if self.status == "Open":
                self.status = "Progress"

    def sync_task_assignments(self):
        """Sync task assignments with project team members"""
        if not self.task:
            return

        try:
            # Get project team members
            team_members = [member.user for member in self.project_team if member.user]

            if not team_members:
                return

            # Update task assignments in child table
            for task_detail in self.task:
                if not task_detail.assigned_to and team_members:
                    # Assign to project lead or first team member
                    task_detail.assigned_to = self.project_lead or team_members[0]

        except Exception as e:
            frappe.log_error(
                f"Error syncing task assignments: {str(e)}", "Project Task Sync Error"
            )

    @frappe.whitelist()
    def get_project_summary(self):
        """Get project summary with task statistics"""
        project_tasks = frappe.get_all(
            "Task",
            filters={"project": self.name, "task_for": "Project"},
            fields=[
                "name",
                "status",
                "priority",
                "expected_start_date",
                "expected_end_date",
            ],
        )

        summary = {
            "total_tasks": len(project_tasks),
            "completed_tasks": len(
                [t for t in project_tasks if t.status == "Completed"]
            ),
            "open_tasks": len([t for t in project_tasks if t.status == "Open"]),
            "working_tasks": len([t for t in project_tasks if t.status == "Working"]),
            "overdue_tasks": len([t for t in project_tasks if t.status == "Overdue"]),
            "progress_percentage": self.progress_rate,
            "status": self.status,
        }

        return summary

    @frappe.whitelist()
    def refresh_project_data(self):
        """Manually refresh project data and task synchronization"""
        try:
            # Update progress rate
            self.update_progress_rate()

            # Sync task assignments
            self.sync_task_assignments()

            # Save changes
            self.save()

            frappe.msgprint("Project data has been refreshed successfully!")

        except Exception as e:
            frappe.throw(f"Error refreshing project data: {str(e)}")
