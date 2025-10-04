from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from datetime import datetime

from app.config import settings
from app.models import (
    AnswerSubmission, AssessmentSession, 
    NextQuestionRequest, NextQuestionResponse, AssessmentComplete,
    DifficultyLevel, SubjectInfo
)
from app.bkt_model import bkt_model
from app.services.question_generator import question_generator
from app.services.storage import storage

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Adaptive learning backend with BKT model and Gemini AI question generation"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins + ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Health"])
async def root():
    return {
        "message": "Adaptive Learning API",
        "version": settings.app_version,
        "engine": "Gemini AI + BKT"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "storage": "In-Memory",
        "ai_engine": "Gemini AI"
    }


@app.get("/api/subjects", response_model=List[SubjectInfo], tags=["Subjects"])
async def get_subjects():
    """Get available subjects for assessment"""
    subjects = [
        SubjectInfo(
            subject="Maths",
            question_count=999,
            topics=["Arithmetic", "Algebra", "Geometry", "Calculus", "Trigonometry"]
        ),
        SubjectInfo(
            subject="Science",
            question_count=999,
            topics=["Biology", "Chemistry", "Physics", "Earth Science", "Astronomy"]
        ),
        SubjectInfo(
            subject="Python",
            question_count=999,
            topics=["Variables", "Functions", "Loops", "OOP", "Data Structures"]
        )
    ]
    return subjects


@app.post("/api/assessment/start", response_model=AssessmentSession, tags=["Assessment"])
async def start_assessment(subject: str, user_id: Optional[str] = None):
    """Start a new adaptive assessment session"""
    if subject not in ["Maths", "Science", "Python"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid subject. Must be one of: Maths, Science, Python"
        )
    
    if not user_id:
        user_id = f"user_{datetime.utcnow().timestamp()}"
    
    session_id = storage.create_session(user_id, subject)
    session_data = storage.get_session(session_id)
    
    return AssessmentSession(
        session_id=session_data["session_id"],
        user_id=session_data["user_id"],
        subject=session_data["subject"],
        created_at=datetime.fromisoformat(session_data["start_time"]),
        is_active=True,
        total_questions=15,
        questions_answered=session_data["total_questions"]
    )


@app.post("/api/assessment/next-question", response_model=NextQuestionResponse, tags=["Assessment"])
async def get_next_question(request: NextQuestionRequest):
    """Get the next adaptive question based on BKT model"""
    session = storage.get_session(request.session_id)
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    if session["status"] != "active":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Session is not active"
        )
    
    if session["total_questions"] >= 15:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Assessment complete. Maximum questions reached."
        )
    
    current_difficulty = session["current_difficulty"]
    mastery_level = session["mastery_level"]
    
    topic = await question_generator.generate_topic_for_subject(
        session["subject"], 
        current_difficulty
    )
    
    previous_questions = storage.get_question_history(request.session_id)
    
    try:
        question_data = await question_generator.generate_question(
            subject=session["subject"],
            topic=topic,
            difficulty=current_difficulty,
            previous_questions=previous_questions
        )
        
        storage.add_question_to_history(request.session_id, question_data["question"])
        storage.store_current_question(request.session_id, question_data)
        
        return NextQuestionResponse(
            session_id=request.session_id,
            question_number=session["total_questions"] + 1,
            total_questions=15,
            current_difficulty=DifficultyLevel(current_difficulty),
            mastery_level=mastery_level,
            question=question_data["question"],
            option_a=question_data["option_a"],
            option_b=question_data["option_b"],
            option_c=question_data["option_c"],
            option_d=question_data["option_d"],
            topic=topic,
            subject=session["subject"]
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate question: {str(e)}"
        )


@app.post("/api/assessment/submit-answer", tags=["Assessment"])
async def submit_answer(submission: AnswerSubmission):
    """Submit an answer and get feedback with BKT update"""
    session = storage.get_session(submission.session_id)
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    if session["status"] != "active":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Session is not active"
        )
    
    current_question = storage.get_current_question(submission.session_id)
    
    if not current_question:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No question has been asked yet"
        )
    
    correct_answer = current_question["correct_answer"]
    explanation = current_question.get("explanation", "")
    topic = current_question.get("topic", submission.topic if submission.topic else "General")
    current_difficulty = current_question.get("difficulty", session["current_difficulty"])
    
    is_correct = submission.selected_answer.upper() == correct_answer
    
    attempt_data = storage.add_attempt(submission.session_id, {
        "question": current_question["question"],
        "selected_answer": submission.selected_answer.upper(),
        "correct_answer": correct_answer,
        "is_correct": is_correct,
        "time_spent": submission.time_spent if submission.time_spent else 0,
        "topic": topic,
        "difficulty": current_difficulty
    })
    
    current_mastery = session["mastery_level"]
    new_mastery = bkt_model.update_mastery(current_mastery, is_correct)
    
    new_difficulty = bkt_model.recommend_difficulty(new_mastery)
    
    new_total = session["total_questions"] + 1
    new_correct = session["correct_answers"] + (1 if is_correct else 0)
    
    storage.update_session(submission.session_id, {
        "total_questions": new_total,
        "correct_answers": new_correct,
        "mastery_level": new_mastery,
        "current_difficulty": new_difficulty
    })
    
    storage.update_user_skill(
        session["user_id"],
        session["subject"],
        topic,
        new_mastery
    )
    
    storage.current_questions.pop(submission.session_id, None)
    
    return {
        "is_correct": is_correct,
        "correct_answer": correct_answer,
        "explanation": explanation,
        "new_mastery_level": round(new_mastery, 2),
        "new_difficulty": new_difficulty,
        "questions_answered": new_total,
        "total_correct": new_correct
    }


@app.post("/api/assessment/complete", response_model=AssessmentComplete, tags=["Assessment"])
async def complete_assessment(session_id: str):
    """Complete an assessment and get learning path recommendations"""
    session = storage.complete_session(session_id)
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    attempts = storage.get_attempts(session_id)
    
    if len(attempts) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No attempts recorded for this session"
        )
    
    total_questions = len(attempts)
    correct_answers = sum(1 for a in attempts if a.get("is_correct", False))
    accuracy = (correct_answers / total_questions * 100) if total_questions > 0 else 0
    
    topic_performance = {}
    for attempt in attempts:
        topic = attempt.get("topic", "General")
        if topic not in topic_performance:
            topic_performance[topic] = {"correct": 0, "total": 0}
        topic_performance[topic]["total"] += 1
        if attempt.get("is_correct", False):
            topic_performance[topic]["correct"] += 1
    
    weak_topics = []
    strong_topics = []
    
    for topic, perf in topic_performance.items():
        if topic and topic != "None":
            topic_accuracy = (perf["correct"] / perf["total"] * 100) if perf["total"] > 0 else 0
            if topic_accuracy < 60:
                weak_topics.append(topic)
            elif topic_accuracy >= 80:
                strong_topics.append(topic)
    
    return AssessmentComplete(
        session_id=session_id,
        total_questions=total_questions,
        correct_answers=correct_answers,
        accuracy=round(accuracy, 2),
        final_mastery_level=round(session["mastery_level"], 2),
        time_taken=0,
        weak_topics=weak_topics,
        strong_topics=strong_topics,
        recommended_resources=[]
    )


@app.get("/api/powerbi/analytics", tags=["Analytics"])
async def get_powerbi_analytics():
    """Get comprehensive analytics data for Power BI dashboard"""
    analytics = storage.get_analytics_data()
    return analytics


@app.get("/api/analytics/subject/{subject}", tags=["Analytics"])
async def get_subject_analytics(subject: str):
    """Get analytics data for a specific subject"""
    if subject not in ["Maths", "Science", "Python"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid subject"
        )
    
    subject_sessions = [s for s in storage.sessions.values() if s["subject"] == subject]
    
    if not subject_sessions:
        return {
            "subject": subject,
            "mastery_estimate": 0.0,
            "growth_data": [],
            "question_history": [],
            "total_questions": 0,
            "correct_answers": 0,
            "accuracy": 0.0
        }
    
    growth_data = []
    all_attempts = []
    total_correct = 0
    total_questions = 0
    
    for session in subject_sessions:
        session_attempts = storage.get_attempts(session["session_id"])
        
        for idx, attempt in enumerate(session_attempts, 1):
            if attempt.get("is_correct"):
                total_correct += 1
            total_questions += 1
            
            growth_data.append({
                "question_number": total_questions,
                "correct": total_correct,
                "accuracy": round((total_correct / total_questions) * 100, 1)
            })
            
            all_attempts.append({
                "question": attempt.get("question", ""),
                "topic": attempt.get("topic", "General"),
                "is_correct": attempt.get("is_correct", False),
                "difficulty": attempt.get("difficulty", "easy"),
                "timestamp": attempt.get("timestamp", "")
            })
    
    subject_skills = [s for s in storage.user_skills.values() if s["subject"] == subject]
    avg_mastery = sum(s["mastery_level"] for s in subject_skills) / len(subject_skills) if subject_skills else 0.0
    
    if not subject_skills and subject_sessions:
        avg_mastery = subject_sessions[-1].get("mastery_level", 0.0)
    
    return {
        "subject": subject,
        "mastery_estimate": round(avg_mastery, 3),
        "growth_data": growth_data,
        "question_history": all_attempts[-20:],
        "total_questions": total_questions,
        "correct_answers": total_correct,
        "accuracy": round((total_correct / total_questions * 100) if total_questions > 0 else 0, 1)
    }


@app.get("/api/user/{user_id}/skills", tags=["User"])
async def get_user_skills(user_id: str):
    """Get all skills for a specific user"""
    skills = storage.get_all_user_skills(user_id)
    return {"user_id": user_id, "skills": skills}


@app.get("/api/learning-path/recommendations", tags=["Learning Path"])
async def get_learning_recommendations(user_id: Optional[str] = None):
    """Generate AI-powered learning recommendations based on quiz performance"""
    
    if not user_id:
        user_sessions = list(storage.sessions.values())
    else:
        user_sessions = [s for s in storage.sessions.values() if s.get("user_id") == user_id]
    
    if not user_sessions:
        return {
            "has_data": False,
            "message": "No quiz data available. Complete a quiz to get personalized recommendations!",
            "recommendations": [],
            "learning_resources": []
        }
    
    all_attempts = []
    subject_performance = {}
    
    for session in user_sessions:
        subject = session["subject"]
        session_attempts = storage.get_attempts(session["session_id"])
        all_attempts.extend(session_attempts)
        
        if subject not in subject_performance:
            subject_performance[subject] = {
                "total": 0,
                "correct": 0,
                "topics": {}
            }
        
        for attempt in session_attempts:
            topic = attempt.get("topic", "General")
            subject_performance[subject]["total"] += 1
            if attempt.get("is_correct"):
                subject_performance[subject]["correct"] += 1
            
            if topic not in subject_performance[subject]["topics"]:
                subject_performance[subject]["topics"][topic] = {"total": 0, "correct": 0}
            subject_performance[subject]["topics"][topic]["total"] += 1
            if attempt.get("is_correct"):
                subject_performance[subject]["topics"][topic]["correct"] += 1
    
    weak_areas = []
    for subject, perf in subject_performance.items():
        accuracy = (perf["correct"] / perf["total"] * 100) if perf["total"] > 0 else 0
        
        for topic, topic_perf in perf["topics"].items():
            topic_accuracy = (topic_perf["correct"] / topic_perf["total"] * 100) if topic_perf["total"] > 0 else 0
            if topic_accuracy < 60:
                weak_areas.append({
                    "subject": subject,
                    "topic": topic,
                    "accuracy": round(topic_accuracy, 1),
                    "questions_attempted": topic_perf["total"]
                })
    
    weak_areas.sort(key=lambda x: x["accuracy"])
    
    prompt = f"""Based on a student's quiz performance, provide personalized learning recommendations.

Performance Data:
"""
    
    for area in weak_areas[:5]:
        prompt += f"- {area['subject']} - {area['topic']}: {area['accuracy']}% accuracy ({area['questions_attempted']} questions)\n"
    
    prompt += """
Please provide:
1. A brief overall assessment (2-3 sentences)
2. Top 3 specific areas to focus on with actionable study tips
3. Recommended study approach

Keep the response concise and encouraging."""
    
    try:
        ai_recommendations = await question_generator.generate_recommendations(prompt)
    except Exception as e:
        ai_recommendations = "Unable to generate AI recommendations at this time."
    
    learning_resources = []
    for area in weak_areas[:3]:
        search_query = f"{area['subject']} {area['topic']} tutorial learn study guide"
        learning_resources.append({
            "subject": area["subject"],
            "topic": area["topic"],
            "accuracy": area["accuracy"],
            "title": f"Learn {area['subject']}: {area['topic']}",
            "description": f"Improve your understanding of {area['topic']} in {area['subject']} (Current: {area['accuracy']}% accuracy)",
            "search_url": f"https://www.google.com/search?q={search_query.replace(' ', '+')}",
            "khan_academy_url": f"https://www.khanacademy.org/search?page_search_query={search_query.replace(' ', '+')}",
            "youtube_url": f"https://www.youtube.com/results?search_query={search_query.replace(' ', '+')}"
        })
    
    return {
        "has_data": True,
        "ai_recommendations": ai_recommendations,
        "weak_areas": weak_areas[:5],
        "learning_resources": learning_resources,
        "total_quizzes": len(user_sessions),
        "total_questions": len(all_attempts)
    }
