import unittest
from models import WorkTask
from task_manager import TaskManager

class TestTaskManager(unittest.TestCase):
    def setUp(self):
        # Изпълнява се преди всеки тест
        self.manager = TaskManager()

    def test_add_task(self):
        task = WorkTask("Test", "Desc", "2025-01-01")
        self.manager.add_task(task)
        self.assertEqual(len(self.manager.tasks), 1)
        self.assertEqual(self.manager.tasks[0].title, "Test")

    def test_find_task(self):
        task = WorkTask("FindMe", "Desc", "2025-01-01")
        self.manager.add_task(task)
        found = self.manager.find_task_by_title("FindMe")
        self.assertIsNotNone(found)
        self.assertEqual(found.title, "FindMe")
    
    def test_complete_task(self):
        task = WorkTask("CompleteMe", "Desc", "2025-01-01")
        self.manager.add_task(task)
        task_to_complete = self.manager.find_task_by_title("CompleteMe")
        task.complete_task()
        self.assertEqual(task_to_complete.get_status(), "Completed")

if __name__ == "__main__":
    unittest.main()