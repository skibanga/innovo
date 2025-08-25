# Copyright (c) 2025, Arnold Simony and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Task(Document):
    def after_insert(self):
        """Add task to project's child table when task is created"""
        if self.project and self.task_for == "Project":
            self.add_task_to_project()

    def on_update(self):
        """Handle task updates"""
        if (
            self.has_value_changed("project")
            and self.project
            and self.task_for == "Project"
        ):
            # Remove from old project if project changed
            if self.get_doc_before_save():
                old_project = self.get_doc_before_save().project
                if old_project and old_project != self.project:
                    self.remove_task_from_project(old_project)

            # Add to new project
            self.add_task_to_project()

        # Update project status when task status changes
        if (
            self.has_value_changed("status")
            and self.project
            and self.task_for == "Project"
        ):
            self.update_project_status()

    def on_trash(self):
        """Remove task from project when task is deleted"""
        if self.project and self.task_for == "Project":
            self.remove_task_from_project(self.project)

    def add_task_to_project(self):
        """Add this task to the project's child table"""
        if not self.project:
            return

        try:
            project_doc = frappe.get_doc("Project", self.project)

            # Check if task already exists in project's child table
            existing_task = None
            for task_detail in project_doc.task:
                if task_detail.task == self.name:
                    existing_task = task_detail
                    break

            if not existing_task:
                # Add new task to project's child table
                project_doc.append(
                    "task",
                    {
                        "task": self.name,
                        "assigned_to": frappe.session.user,  # Default to current user
                        "expected_to_start": self.expected_start_date,
                        "expected_to_end": self.expected_end_date,
                        "description": self.task_description or self.subject,
                        "status": self.status,
                    },
                )

                project_doc.flags.ignore_permissions = True
                project_doc.save()

                frappe.msgprint(
                    f"Task '{self.subject}' has been added to project '{project_doc.project_title}'"
                )

        except Exception as e:
            frappe.log_error(
                f"Error adding task to project: {str(e)}", "Task to Project Error"
            )

    def remove_task_from_project(self, project_name):
        """Remove this task from the project's child table"""
        try:
            project_doc = frappe.get_doc("Project", project_name)

            # Find and remove the task from project's child table
            for i, task_detail in enumerate(project_doc.task):
                if task_detail.task == self.name:
                    project_doc.task.pop(i)
                    break

            project_doc.flags.ignore_permissions = True
            project_doc.save()

            # Update project status after removing task
            self.check_and_update_project_completion(project_name)

        except Exception as e:
            frappe.log_error(
                f"Error removing task from project: {str(e)}", "Task Removal Error"
            )

    def update_project_status(self):
        """Update project status based on task completion"""
        if not self.project:
            return

        self.check_and_update_project_completion(self.project)

    def check_and_update_project_completion(self, project_name):
        """Check if all project tasks are completed and update project status"""
        try:
            # Get all tasks for this project
            project_tasks = frappe.get_all(
                "Task",
                filters={"project": project_name, "task_for": "Project"},
                fields=["name", "status"],
            )

            if not project_tasks:
                return

            # Check if all tasks are completed
            completed_tasks = [
                task for task in project_tasks if task.status == "Completed"
            ]
            total_tasks = len(project_tasks)
            completed_count = len(completed_tasks)

            # Calculate progress percentage
            progress_rate = (
                (completed_count / total_tasks) * 100 if total_tasks > 0 else 0
            )

            # Update project
            project_doc = frappe.get_doc("Project", project_name)
            project_doc.progress_rate = progress_rate

            # Update project status based on completion
            if completed_count == total_tasks:
                project_doc.status = "Completed"
                if not project_doc.completed_date:
                    project_doc.completed_date = frappe.utils.today()
                frappe.msgprint(
                    f"Project '{project_doc.project_title}' has been automatically marked as Completed!"
                )
            elif completed_count > 0:
                if project_doc.status == "Open":
                    project_doc.status = "Progress"

            project_doc.flags.ignore_permissions = True
            project_doc.save()

        except Exception as e:
            frappe.log_error(
                f"Error updating project status: {str(e)}",
                "Project Status Update Error",
            )
