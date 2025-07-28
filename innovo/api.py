# Innovo API functions
import frappe  # pyright: ignore[reportMissingImports]


@frappe.whitelist()
def add_task_to_project(task_name, project_name):
    """Add a task to project's child table manually"""
    try:
        task_doc = frappe.get_doc("Task", task_name)
        project_doc = frappe.get_doc("Project", project_name)

        # Check for duplicates in the correct child table field
        existing_task = None
        for task_detail in project_doc.task:  # Correct field name is 'task'
            if task_detail.task == task_name:
                existing_task = task_detail
                break

        if not existing_task:
            project_doc.append(
                "task",
                {  # Correct field name is 'task'
                    "task": task_name,
                    "assigned_to": frappe.session.user,
                    "expected_to_start": task_doc.expected_start_date,
                    "expected_to_end": task_doc.expected_end_date,
                    "description": task_doc.task_description or task_doc.subject,
                },
            )

            project_doc.save(ignore_permissions=True)

            # Update task's project field if not already set
            if not task_doc.project:
                task_doc.project = project_name
                task_doc.save(ignore_permissions=True)

            return {
                "success": True,
                "message": f"Task '{task_doc.subject}' added to project '{project_doc.project_title}'",
            }

        return {"success": False, "message": "Task already exists in this project"}

    except Exception as e:
        frappe.log_error(f"Error in add_task_to_project: {str(e)}", "API Error")
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def get_project_tasks_summary(project_name):
    """Get summary of all tasks for a project"""
    try:
        project_doc = frappe.get_doc("Project", project_name)

        # Get all tasks from Task doctype
        project_tasks = frappe.get_all(
            "Task",
            filters={"project": project_name, "task_for": "Project"},
            fields=[
                "name",
                "subject",
                "status",
                "priority",
                "expected_start_date",
                "expected_end_date",
            ],
        )

        # Get tasks from project's child table
        child_table_tasks = []
        for task_detail in project_doc.task:
            child_table_tasks.append(
                {
                    "task": task_detail.task,
                    "assigned_to": task_detail.assigned_to,
                    "team_name": task_detail.team_name,
                    "expected_to_start": task_detail.expected_to_start,
                    "expected_to_end": task_detail.expected_to_end,
                    "description": task_detail.description,
                }
            )

        summary = {
            "project_title": project_doc.project_title,
            "project_status": project_doc.status,
            "progress_rate": project_doc.progress_rate,
            "total_tasks": len(project_tasks),
            "completed_tasks": len(
                [t for t in project_tasks if t.status == "Completed"]
            ),
            "task_details": project_tasks,
            "child_table_tasks": child_table_tasks,
        }

        return summary

    except Exception as e:
        frappe.log_error(f"Error in get_project_tasks_summary: {str(e)}", "API Error")
        return {"error": str(e)}


@frappe.whitelist()
def sync_project_tasks(project_name):
    """Manually sync all project tasks between Task doctype and Project child table"""
    try:
        project_doc = frappe.get_doc("Project", project_name)

        # Get all tasks for this project
        project_tasks = frappe.get_all(
            "Task",
            filters={"project": project_name, "task_for": "Project"},
            fields=[
                "name",
                "subject",
                "expected_start_date",
                "expected_end_date",
                "task_description",
            ],
        )

        # Clear existing child table
        project_doc.task = []

        # Add all tasks to child table
        for task in project_tasks:
            project_doc.append(
                "task",
                {
                    "task": task.name,
                    "assigned_to": frappe.session.user,
                    "expected_to_start": task.expected_start_date,
                    "expected_to_end": task.expected_end_date,
                    "description": task.task_description or task.subject,
                },
            )

        project_doc.save(ignore_permissions=True)

        return {
            "success": True,
            "message": f"Synced {len(project_tasks)} tasks for project '{project_doc.project_title}'",
        }

    except Exception as e:
        frappe.log_error(f"Error in sync_project_tasks: {str(e)}", "API Error")
        return {"success": False, "message": str(e)}
