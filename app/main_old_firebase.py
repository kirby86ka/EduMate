from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import uuid
from datetime import datetime
import random

from app.config import settings
from app.database import db_manager
from app.models import (
    Question, AnswerSubmission, AssessmentSession, Attempt,
    UserSkill, LearningPath, LearningPathTopic, SubjectInfo,
    NextQuestionRequest, NextQuestionResponse, AssessmentComplete,
    DifficultyLevel
)
from app.bkt_model import bkt_model
from app.auth import verify_admin_key, verify_ai_key

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Adaptive learning backend with BKT model for personalized assessments"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    await db_manager.connect()


@app.on_event("shutdown")
async def shutdown_event():
    await db_manager.close()


@app.get("/", tags=["Health"])
async def root():
    return {
        "message": "Adaptive Learning API",
        "version": settings.app_version,
        "database": "Firebase Firestore"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "database": "Firebase Firestore"
    }


@app.get("/api/subjects", response_model=List[SubjectInfo], tags=["Subjects"])
async def get_subjects():
    questions_collection = db_manager.get_collection("questions")
    questions = await questions_collection.find({}).to_list(length=None)
    
    subjects_dict = {}
    for q in questions:
        subject = q.get("subject", "Unknown")
        topic = q.get("topic", "General")
        
        if subject not in subjects_dict:
            subjects_dict[subject] = {
                "subject": subject,
                "question_count": 0,
                "topics": set()
            }
        
        subjects_dict[subject]["question_count"] += 1
        subjects_dict[subject]["topics"].add(topic)
    
    subjects_list = []
    for subject_data in subjects_dict.values():
        subjects_list.append(SubjectInfo(
            subject=subject_data["subject"],
            question_count=subject_data["question_count"],
            topics=sorted(list(subject_data["topics"]))
        ))
    
    return subjects_list


@app.post("/api/assessment/start", response_model=AssessmentSession, tags=["Assessment"])
async def start_assessment(subject: str, user_id: Optional[str] = None):
    questions_collection = db_manager.get_collection("questions")
    question_count = await questions_collection.count_documents({"subject": subject})
    
    if question_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No questions found for subject: {subject}"
        )
    
    session_id = str(uuid.uuid4())
    
    session_data = {
        "session_id": session_id,
        "user_id": user_id,
        "subject": subject,
        "created_at": datetime.utcnow(),
        "is_active": True,
        "total_questions": 15,
        "questions_answered": 0
    }
    
    sessions_collection = db_manager.get_collection("sessions")
    result = await sessions_collection.insert_one(session_data)
    session_data["_id"] = result.inserted_id
    
    return AssessmentSession(**session_data)


@app.post("/api/assessment/next-question", response_model=NextQuestionResponse, tags=["Assessment"])
async def get_next_question(request: NextQuestionRequest):
    sessions_collection = db_manager.get_collection("sessions")
    session = await sessions_collection.find_one({"session_id": request.session_id})
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    if not session.get("is_active", False):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Session is no longer active"
        )
    
    questions_answered = session.get("questions_answered", 0)
    total_questions = session.get("total_questions", 15)
    
    if questions_answered >= total_questions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Assessment already completed"
        )
    
    topic_mastery = await bkt_model.get_topic_mastery(request.session_id)
    
    if topic_mastery:
        avg_mastery = sum(topic_mastery.values()) / len(topic_mastery)
        recommended_difficulty = bkt_model.recommend_difficulty(avg_mastery)
    else:
        recommended_difficulty = DifficultyLevel.EASY
    
    attempts_collection = db_manager.get_collection("attempts")
    answered_questions = await attempts_collection.find(
        {"session_id": request.session_id}
    ).to_list(length=None)
    answered_ids = {att["question_id"] for att in answered_questions}
    
    questions_collection = db_manager.get_collection("questions")
    available_questions = await questions_collection.find({
        "subject": session["subject"],
        "difficulty": recommended_difficulty
    }).to_list(length=None)
    
    available_questions = [q for q in available_questions if q.get("_id") not in answered_ids]
    
    if not available_questions:
        all_questions = await questions_collection.find({
            "subject": session["subject"]
        }).to_list(length=None)
        available_questions = [q for q in all_questions if q.get("_id") not in answered_ids]
    
    if not available_questions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No more questions available"
        )
    
    selected_question = random.choice(available_questions)
    
    return NextQuestionResponse(
        question=Question(**selected_question),
        question_number=questions_answered + 1,
        total_questions=total_questions,
        can_request_more=questions_answered + 1 < total_questions
    )


@app.post("/api/assessment/submit-answer", tags=["Assessment"])
async def submit_answer(submission: AnswerSubmission):
    sessions_collection = db_manager.get_collection("sessions")
    session = await sessions_collection.find_one({"session_id": submission.session_id})
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    questions_collection = db_manager.get_collection("questions")
    question = await questions_collection.find_one({"_id": submission.question_id})
    
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    
    is_correct = submission.selected_answer.upper() == question["correct_answer"].upper()
    
    attempt_data = {
        "session_id": submission.session_id,
        "question_id": submission.question_id,
        "selected_answer": submission.selected_answer,
        "correct_answer": question["correct_answer"],
        "is_correct": is_correct,
        "difficulty": question["difficulty"],
        "topic": question.get("topic", "General"),
        "time_taken_seconds": submission.time_taken_seconds,
        "answered_at": datetime.utcnow()
    }
    
    attempts_collection = db_manager.get_collection("attempts")
    await attempts_collection.insert_one(attempt_data)
    
    topic = question.get("topic", "General")
    await bkt_model.update_user_skill(
        session_id=submission.session_id,
        topic=topic,
        subject=question["subject"],
        is_correct=is_correct,
        user_id=session.get("user_id")
    )
    
    await sessions_collection.update_one(
        {"session_id": submission.session_id},
        {"$inc": {"questions_answered": 1}}
    )
    
    return {
        "success": True,
        "is_correct": is_correct,
        "correct_answer": question["correct_answer"],
        "topic": topic
    }


@app.post("/api/assessment/complete", response_model=AssessmentComplete, tags=["Assessment"])
async def complete_assessment(session_id: str):
    sessions_collection = db_manager.get_collection("sessions")
    session = await sessions_collection.find_one({"session_id": session_id})
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    await sessions_collection.update_one(
        {"session_id": session_id},
        {
            "$set": {
                "is_active": False,
                "completed_at": datetime.utcnow()
            }
        }
    )
    
    attempts_collection = db_manager.get_collection("attempts")
    attempts = await attempts_collection.find({"session_id": session_id}).to_list(length=None)
    
    total_answered = len(attempts)
    correct_count = sum(1 for att in attempts if att.get("is_correct", False))
    score = (correct_count / total_answered * 100) if total_answered > 0 else 0
    
    return AssessmentComplete(
        session_id=session_id,
        total_answered=total_answered,
        score=score,
        message=f"Assessment completed. Score: {score:.1f}%"
    )


@app.get("/api/learning-path/{session_id}", response_model=LearningPath, tags=["Learning Path"])
async def get_learning_path(session_id: str):
    sessions_collection = db_manager.get_collection("sessions")
    session = await sessions_collection.find_one({"session_id": session_id})
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    attempts_collection = db_manager.get_collection("attempts")
    attempts = await attempts_collection.find({"session_id": session_id}).to_list(length=None)
    
    if not attempts:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No attempts found for this session"
        )
    
    topic_mastery = await bkt_model.get_topic_mastery(session_id)
    
    total_attempts = len(attempts)
    correct_attempts = sum(1 for att in attempts if att.get("is_correct", False))
    overall_score = (correct_attempts / total_attempts) if total_attempts > 0 else 0
    
    weak_topics = []
    strong_topics = []
    
    for topic, mastery in topic_mastery.items():
        if mastery < 0.5:
            recommended_difficulty = bkt_model.recommend_difficulty(mastery)
            weak_topics.append(LearningPathTopic(
                topic=topic,
                mastery_score=mastery,
                priority="high" if mastery < 0.3 else "medium",
                recommended_difficulty=recommended_difficulty,
                questions_to_practice=10 if mastery < 0.3 else 5
            ))
        else:
            strong_topics.append(topic)
    
    weak_topics.sort(key=lambda x: x.mastery_score)
    
    course_outline = []
    course_outline.append(f"Review and strengthen weak topics: {', '.join([t.topic for t in weak_topics[:3]])}")
    course_outline.append("Practice with adaptive difficulty questions")
    course_outline.append("Focus on understanding core concepts")
    if strong_topics:
        course_outline.append(f"Advanced topics to explore: {', '.join(strong_topics[:3])}")
    
    return LearningPath(
        session_id=session_id,
        subject=session["subject"],
        overall_score=overall_score,
        mastery_by_topic=topic_mastery,
        weak_topics=weak_topics,
        strong_topics=strong_topics,
        recommended_course_outline=course_outline
    )


@app.post("/api/admin/questions", response_model=Question, tags=["Admin"], dependencies=[Depends(verify_admin_key)])
async def add_question(question: Question):
    questions_collection = db_manager.get_collection("questions")
    
    question_dict = question.model_dump(exclude={"id"})
    result = await questions_collection.insert_one(question_dict)
    question_dict["_id"] = result.inserted_id
    
    return Question(**question_dict)


@app.post("/api/admin/questions/bulk", tags=["Admin"], dependencies=[Depends(verify_admin_key)])
async def bulk_add_questions(questions: List[Question]):
    questions_collection = db_manager.get_collection("questions")
    
    questions_data = [q.model_dump(exclude={"id"}) for q in questions]
    result = await questions_collection.insert_many(questions_data)
    
    return {
        "success": True,
        "inserted_count": len(result.inserted_ids),
        "inserted_ids": [str(id) for id in result.inserted_ids]
    }


@app.get("/api/admin/sessions", tags=["Admin"], dependencies=[Depends(verify_admin_key)])
async def get_all_sessions():
    sessions_collection = db_manager.get_collection("sessions")
    sessions = await sessions_collection.find({}).to_list(length=None)
    return {"sessions": sessions, "count": len(sessions)}


@app.get("/api/admin/analytics/{session_id}", tags=["Admin"], dependencies=[Depends(verify_admin_key)])
async def get_session_analytics(session_id: str):
    sessions_collection = db_manager.get_collection("sessions")
    session = await sessions_collection.find_one({"session_id": session_id})
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    attempts_collection = db_manager.get_collection("attempts")
    attempts = await attempts_collection.find({"session_id": session_id}).to_list(length=None)
    
    skills_collection = db_manager.get_collection("user_skills")
    skills = await skills_collection.find({"session_id": session_id}).to_list(length=None)
    
    return {
        "session": session,
        "attempts": attempts,
        "user_skills": skills,
        "total_attempts": len(attempts),
        "correct_attempts": sum(1 for att in attempts if att.get("is_correct", False))
    }


@app.post("/api/ai/ingest", tags=["AI/ML"], dependencies=[Depends(verify_ai_key)])
async def ai_ingest_endpoint(data: dict):
    return {
        "success": True,
        "message": "AI ingest endpoint - ready for ML model integration",
        "received_data": data
    }


@app.get("/api/powerbi/analytics", tags=["Power BI"], dependencies=[Depends(verify_admin_key)])
async def get_powerbi_analytics():
    """
    Comprehensive analytics endpoint for Power BI dashboard integration.
    Returns aggregated data including sessions, attempts, performance metrics, and mastery scores.
    """
    sessions_collection = db_manager.get_collection("sessions")
    attempts_collection = db_manager.get_collection("attempts")
    skills_collection = db_manager.get_collection("user_skills")
    questions_collection = db_manager.get_collection("questions")
    
    all_sessions = await sessions_collection.find({}).to_list(length=None)
    all_attempts = await attempts_collection.find({}).to_list(length=None)
    all_skills = await skills_collection.find({}).to_list(length=None)
    all_questions = await questions_collection.find({}).to_list(length=None)
    
    overall_metrics = {
        "total_sessions": len(all_sessions),
        "total_attempts": len(all_attempts),
        "total_questions": len(all_questions),
        "total_users": len(set(s.get("user_id") for s in all_sessions if s.get("user_id"))),
        "completed_sessions": len([s for s in all_sessions if not s.get("is_active", True)]),
        "active_sessions": len([s for s in all_sessions if s.get("is_active", True)]),
    }
    
    correct_attempts = [a for a in all_attempts if a.get("is_correct", False)]
    overall_metrics["overall_accuracy"] = (len(correct_attempts) / len(all_attempts) * 100) if all_attempts else 0
    
    subject_performance = {}
    for session in all_sessions:
        subject = session.get("subject", "Unknown")
        if subject not in subject_performance:
            subject_performance[subject] = {
                "subject": subject,
                "total_sessions": 0,
                "total_attempts": 0,
                "correct_attempts": 0,
                "accuracy": 0.0,
                "avg_mastery": 0.0
            }
        
        subject_performance[subject]["total_sessions"] += 1
        session_attempts = [a for a in all_attempts if a.get("session_id") == session.get("session_id")]
        subject_performance[subject]["total_attempts"] += len(session_attempts)
        subject_performance[subject]["correct_attempts"] += len([a for a in session_attempts if a.get("is_correct", False)])
    
    for subject, data in subject_performance.items():
        if data["total_attempts"] > 0:
            data["accuracy"] = (data["correct_attempts"] / data["total_attempts"] * 100)
        
        subject_skills = [s for s in all_skills if s.get("subject") == subject]
        if subject_skills:
            data["avg_mastery"] = sum(s.get("mastery_probability", 0) for s in subject_skills) / len(subject_skills)
    
    topic_performance = {}
    for skill in all_skills:
        topic = skill.get("topic", "Unknown")
        if topic not in topic_performance:
            topic_performance[topic] = {
                "topic": topic,
                "subject": skill.get("subject", "Unknown"),
                "total_learners": 0,
                "avg_mastery": 0.0,
                "total_attempts": 0,
                "correct_attempts": 0,
                "accuracy": 0.0
            }
        
        topic_performance[topic]["total_learners"] += 1
        topic_performance[topic]["avg_mastery"] += skill.get("mastery_probability", 0)
        topic_performance[topic]["total_attempts"] += skill.get("attempts_count", 0)
        topic_performance[topic]["correct_attempts"] += skill.get("correct_count", 0)
    
    for topic, data in topic_performance.items():
        if data["total_learners"] > 0:
            data["avg_mastery"] = data["avg_mastery"] / data["total_learners"]
        if data["total_attempts"] > 0:
            data["accuracy"] = (data["correct_attempts"] / data["total_attempts"] * 100)
    
    difficulty_distribution = {
        "easy": {"total": 0, "correct": 0, "accuracy": 0.0},
        "medium": {"total": 0, "correct": 0, "accuracy": 0.0},
        "hard": {"total": 0, "correct": 0, "accuracy": 0.0}
    }
    
    for attempt in all_attempts:
        difficulty = attempt.get("difficulty", "medium")
        if difficulty in difficulty_distribution:
            difficulty_distribution[difficulty]["total"] += 1
            if attempt.get("is_correct", False):
                difficulty_distribution[difficulty]["correct"] += 1
    
    for diff, data in difficulty_distribution.items():
        if data["total"] > 0:
            data["accuracy"] = (data["correct"] / data["total"] * 100)
    
    time_series_data = []
    for attempt in all_attempts:
        time_series_data.append({
            "timestamp": attempt.get("answered_at"),
            "session_id": attempt.get("session_id"),
            "is_correct": attempt.get("is_correct", False),
            "difficulty": attempt.get("difficulty"),
            "topic": attempt.get("topic"),
            "time_taken_seconds": attempt.get("time_taken_seconds")
        })
    
    return {
        "overview": overall_metrics,
        "subject_performance": list(subject_performance.values()),
        "topic_performance": list(topic_performance.values()),
        "difficulty_distribution": [
            {"difficulty": k, **v} for k, v in difficulty_distribution.items()
        ],
        "time_series_data": time_series_data,
        "generated_at": datetime.utcnow().isoformat()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
