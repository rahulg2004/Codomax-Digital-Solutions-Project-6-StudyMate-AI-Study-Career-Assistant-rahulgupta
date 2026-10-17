def build_study_plan(subjects, days_left, hours_per_day, level):
    return f"""
You are a study-planning assistant. Build a practical schedule with breaks and active recall.
Subjects/topics: {subjects}
Days available: {days_left}
Available study time per day: {hours_per_day} hours
Preparation level: {level}

Include:
1. A brief strategy and prioritisation approach.
2. A day-by-day table with topics, focused study blocks, practice, and revision.
3. Daily active-recall tasks.
4. A final revision and self-test plan.
5. A realistic buffer for difficult topics.
Avoid scheduling more than the available hours. If the workload is too large, explain the trade-offs.
"""

def make_quiz_prompt(topic, difficulty, count, question_type):
    return f"""
Create a high-quality educational practice quiz.
Topic: {topic}
Difficulty: {difficulty}
Number of questions: {count}
Question style: {question_type}

Requirements:
- Number every question.
- For multiple-choice questions, provide four options labelled A-D.
- Put the answer key and concise explanations in a separate section at the end.
- Avoid ambiguous questions and ensure there is one clearly correct answer for each MCQ.
- Include a mix of recall and application questions when appropriate.
"""

def route_agent_task(user_request):
    """
    Simple, transparent agent-style router. It maps a request to a dedicated workflow.
    This is a deterministic tool router, not an autonomous multi-agent system.
    """
    request = user_request.lower()
    if any(word in request for word in ["study plan", "schedule", "timetable", "revision plan"]):
        return "study_planner"
    if any(word in request for word in ["quiz", "mcq", "practice questions", "test me"]):
        return "quiz_generator"
    if any(word in request for word in ["career", "resume", "interview", "job roadmap"]):
        return "career_assistant"
    if any(word in request for word in ["pdf", "document", "uploaded file", "notes"]):
        return "document_rag"
    return "general_chat"
