import unittest
from modules.tools import route_agent_task, build_study_plan, make_quiz_prompt

class ToolTests(unittest.TestCase):
    def test_routes_study_plan(self):
        self.assertEqual(route_agent_task("make a study plan"), "study_planner")

    def test_routes_quiz(self):
        self.assertEqual(route_agent_task("create an MCQ quiz"), "quiz_generator")

    def test_routes_career(self):
        self.assertEqual(route_agent_task("help with my career roadmap"), "career_assistant")

    def test_routes_pdf(self):
        self.assertEqual(route_agent_task("ask about this PDF document"), "document_rag")

    def test_default_route(self):
        self.assertEqual(route_agent_task("explain recursion"), "general_chat")

    def test_study_plan_contains_constraints(self):
        prompt = build_study_plan("DBMS", 5, 2, "Revision")
        self.assertIn("DBMS", prompt)
        self.assertIn("5", prompt)
        self.assertIn("2 hours", prompt)

    def test_quiz_contains_count(self):
        prompt = make_quiz_prompt("Regression", "Medium", 5, "Multiple choice")
        self.assertIn("5", prompt)
        self.assertIn("Regression", prompt)

if __name__ == "__main__":
    unittest.main()
