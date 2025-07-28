# Copyright (c) 2025, Arnold Simony and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase


class TestTask(FrappeTestCase):
    def setUp(self):
        """Set up test data"""
        # Create a test project
        if not frappe.db.exists("Project", "TEST-PROJ-001"):
            self.test_project = frappe.get_doc(
                {
                    "doctype": "Project",
                    "naming_series": "PROJ-.####",
                    "project_title": "Test Project for Task Integration",
                    "category": "Import",
                    "status": "Open",
                    "client": self.create_test_customer(),
                    "project_lead": "Administrator",
                    "kickoff_date": frappe.utils.today(),
                    "progress_rate": 0,
                }
            )
            self.test_project.insert()
        else:
            self.test_project = frappe.get_doc("Project", "TEST-PROJ-001")

    def create_test_customer(self):
        """Create a test customer if it doesn't exist"""
        if not frappe.db.exists("Customer", "Test Customer"):
            customer = frappe.get_doc(
                {
                    "doctype": "Customer",
                    "customer_name": "Test Customer",
                    "customer_type": "Company",
                }
            )
            customer.insert()
            return customer.name
        return "Test Customer"

    def test_task_auto_add_to_project(self):
        """Test that tasks are automatically added to project child table"""
        # Create a task for the project
        task = frappe.get_doc(
            {
                "doctype": "Task",
                "subject": "Test Task for Auto Add",
                "task_for": "Project",
                "project": self.test_project.name,
                "status": "Open",
                "priority": "Important",
                "expected_start_date": frappe.utils.today(),
                "expected_end_date": frappe.utils.add_days(frappe.utils.today(), 7),
                "task_description": "This is a test task for auto-add functionality",
            }
        )
        task.insert()

        # Reload project and check if task was added to child table
        self.test_project.reload()
        task_found = False
        for task_detail in self.test_project.task:
            if task_detail.task == task.name:
                task_found = True
                break

        self.assertTrue(
            task_found, "Task should be automatically added to project child table"
        )

        # Clean up
        task.delete()

    def test_project_auto_completion(self):
        """Test that project status changes to Completed when all tasks are completed"""
        # Create multiple tasks for the project
        tasks = []
        for i in range(3):
            task = frappe.get_doc(
                {
                    "doctype": "Task",
                    "subject": f"Test Task {i+1} for Completion",
                    "task_for": "Project",
                    "project": self.test_project.name,
                    "status": "Open",
                    "priority": "Important",
                    "expected_start_date": frappe.utils.today(),
                    "expected_end_date": frappe.utils.add_days(frappe.utils.today(), 7),
                }
            )
            task.insert()
            tasks.append(task)

        # Mark all tasks as completed
        for task in tasks:
            task.status = "Completed"
            task.save()

        # Reload project and check status
        self.test_project.reload()
        self.assertEqual(
            self.test_project.status,
            "Completed",
            "Project should be automatically marked as Completed",
        )
        self.assertEqual(
            self.test_project.progress_rate, 100, "Project progress should be 100%"
        )

        # Clean up
        for task in tasks:
            task.delete()

    def test_project_progress_calculation(self):
        """Test that project progress is calculated correctly"""
        # Create 4 tasks
        tasks = []
        for i in range(4):
            task = frappe.get_doc(
                {
                    "doctype": "Task",
                    "subject": f"Progress Test Task {i+1}",
                    "task_for": "Project",
                    "project": self.test_project.name,
                    "status": "Open",
                    "priority": "Important",
                    "expected_start_date": frappe.utils.today(),
                    "expected_end_date": frappe.utils.add_days(frappe.utils.today(), 7),
                }
            )
            task.insert()
            tasks.append(task)

        # Complete 2 out of 4 tasks (50%)
        for i in range(2):
            tasks[i].status = "Completed"
            tasks[i].save()

        # Check progress
        self.test_project.reload()
        self.assertEqual(
            self.test_project.progress_rate, 50, "Project progress should be 50%"
        )
        self.assertEqual(
            self.test_project.status, "Progress", "Project status should be Progress"
        )

        # Clean up
        for task in tasks:
            task.delete()

    def tearDown(self):
        """Clean up test data"""
        # Delete test project if it exists
        if frappe.db.exists("Project", self.test_project.name):
            # First delete all associated tasks
            tasks = frappe.get_all("Task", filters={"project": self.test_project.name})
            for task in tasks:
                frappe.delete_doc("Task", task.name)

            # Then delete the project
            frappe.delete_doc("Project", self.test_project.name)
