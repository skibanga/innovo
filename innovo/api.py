# In your_app/api.py
import frappe # pyright: ignore[reportMissingImports]

@frappe.whitelist()
def add_task_to_project(task_name, project_name):
    task_doc = frappe.get_doc("Task", task_name)
    project_doc = frappe.get_doc("Project", project_name)

    # Check for duplicates
    existing_task = next((task for task in project_doc.tasks if task.task == task_name), None)

    if not existing_task:
        project_doc.append("tasks", {
            "task": task_name,
            "subject": task_doc.subject,
            "status": task_doc.status,
            "start_date": task_doc.exp_start_date,
            "end_date": task_doc.exp_end_date
        })

        project_doc.save(ignore_permissions=True)
        return True

    return False
