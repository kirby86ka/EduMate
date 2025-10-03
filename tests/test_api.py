import pytest
from httpx import ASGITransport, AsyncClient
from app.main import app
from app.database import db_manager


@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.fixture(autouse=True)
async def setup_database():
    await db_manager.connect()
    
    questions_collection = db_manager.get_collection("questions")
    await questions_collection.delete_many({})
    
    test_questions = [
        {
            "_id": "q1",
            "question": "What is Python?",
            "option_a": "A snake",
            "option_b": "A programming language",
            "option_c": "A framework",
            "option_d": "A database",
            "correct_answer": "B",
            "difficulty": "easy",
            "subject": "Python",
            "topic": "Basics"
        },
        {
            "_id": "q2",
            "question": "What is a list?",
            "option_a": "An array",
            "option_b": "A tuple",
            "option_c": "A mutable sequence",
            "option_d": "A string",
            "correct_answer": "C",
            "difficulty": "medium",
            "subject": "Python",
            "topic": "Data Structures"
        }
    ]
    await questions_collection.insert_many(test_questions)
    
    yield
    
    sessions_collection = db_manager.get_collection("sessions")
    attempts_collection = db_manager.get_collection("attempts")
    skills_collection = db_manager.get_collection("user_skills")
    
    await sessions_collection.delete_many({})
    await attempts_collection.delete_many({})
    await skills_collection.delete_many({})


@pytest.mark.asyncio
async def test_health_check(client):
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


@pytest.mark.asyncio
async def test_get_subjects(client):
    response = await client.get("/api/subjects")
    assert response.status_code == 200
    subjects = response.json()
    assert len(subjects) > 0
    assert any(s["subject"] == "Python" for s in subjects)


@pytest.mark.asyncio
async def test_start_assessment(client):
    response = await client.post("/api/assessment/start?subject=Python")
    assert response.status_code == 200
    data = response.json()
    assert "session_id" in data
    assert data["subject"] == "Python"
    assert data["is_active"] is True


@pytest.mark.asyncio
async def test_assessment_workflow(client):
    start_response = await client.post("/api/assessment/start?subject=Python")
    assert start_response.status_code == 200
    session_data = start_response.json()
    session_id = session_data["session_id"]
    
    next_q_response = await client.post(
        "/api/assessment/next-question",
        json={"session_id": session_id}
    )
    assert next_q_response.status_code == 200
    question_data = next_q_response.json()
    assert "question" in question_data
    question_id = question_data["question"]["_id"]
    
    submit_response = await client.post(
        "/api/assessment/submit-answer",
        json={
            "session_id": session_id,
            "question_id": question_id,
            "selected_answer": "B"
        }
    )
    assert submit_response.status_code == 200
    submit_data = submit_response.json()
    assert "success" in submit_data
    assert submit_data["success"] is True


@pytest.mark.asyncio
async def test_complete_assessment(client):
    start_response = await client.post("/api/assessment/start?subject=Python")
    session_id = start_response.json()["session_id"]
    
    next_q_response = await client.post(
        "/api/assessment/next-question",
        json={"session_id": session_id}
    )
    question_id = next_q_response.json()["question"]["_id"]
    
    await client.post(
        "/api/assessment/submit-answer",
        json={
            "session_id": session_id,
            "question_id": question_id,
            "selected_answer": "B"
        }
    )
    
    complete_response = await client.post(
        f"/api/assessment/complete?session_id={session_id}"
    )
    assert complete_response.status_code == 200
    complete_data = complete_response.json()
    assert "score" in complete_data
    assert complete_data["total_answered"] == 1


@pytest.mark.asyncio
async def test_learning_path(client):
    start_response = await client.post("/api/assessment/start?subject=Python")
    session_id = start_response.json()["session_id"]
    
    next_q_response = await client.post(
        "/api/assessment/next-question",
        json={"session_id": session_id}
    )
    question_id = next_q_response.json()["question"]["_id"]
    
    await client.post(
        "/api/assessment/submit-answer",
        json={
            "session_id": session_id,
            "question_id": question_id,
            "selected_answer": "B"
        }
    )
    
    path_response = await client.get(f"/api/learning-path/{session_id}")
    assert path_response.status_code == 200
    path_data = path_response.json()
    assert "overall_score" in path_data
    assert "weak_topics" in path_data
    assert "strong_topics" in path_data


@pytest.mark.asyncio
async def test_admin_add_question(client):
    response = await client.post(
        "/api/admin/questions",
        headers={"X-API-Key": "admin-key-change-in-production"},
        json={
            "question": "Test question?",
            "option_a": "Option A",
            "option_b": "Option B",
            "option_c": "Option C",
            "option_d": "Option D",
            "correct_answer": "A",
            "difficulty": "easy",
            "subject": "Test",
            "topic": "Testing"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["question"] == "Test question?"


@pytest.mark.asyncio
async def test_admin_unauthorized(client):
    response = await client.post(
        "/api/admin/questions",
        headers={"X-API-Key": "wrong-key"},
        json={
            "question": "Test",
            "option_a": "A",
            "option_b": "B",
            "option_c": "C",
            "option_d": "D",
            "correct_answer": "A",
            "difficulty": "easy",
            "subject": "Test"
        }
    )
    assert response.status_code == 403
