# Adaptive Learning API Documentation

## Overview

This is a FastAPI backend implementing an adaptive learning workflow with Bayesian Knowledge Tracing (BKT) for personalized assessments. The system adapts question difficulty based on user performance and generates personalized learning paths.

**Base URL**: `http://localhost:5000` (Development)  
**Database**: MongoDB with in-memory fallback  
**Authentication**: API Key (for admin/AI routes)

---

## Architecture

### Components

1. **FastAPI Application** - REST API server with OpenAPI documentation
2. **MongoDB/In-Memory Database** - Question bank, sessions, attempts, user skills
3. **BKT Model** - Bayesian Knowledge Tracing for adaptive question selection
4. **CORS** - Enabled for `http://localhost:3000`

### Data Flow

```
User → Start Assessment → Get Questions (BKT-adapted) → Submit Answers → 
BKT Updates Mastery → Complete Assessment → Get Learning Path
```

---

## For Frontend Developers

### Typical User Journey

1. **Get Available Subjects**
2. **Start Assessment** for chosen subject
3. **Loop**: Get next question → Display to user → Submit answer
4. **Complete Assessment** when done
5. **Get Learning Path** to show personalized recommendations

### Key Endpoints for Frontend

#### 1. Get Subjects List

```http
GET /api/subjects
```

**Response:**
```json
[
  {
    "subject": "Python",
    "question_count": 20,
    "topics": ["Data Structures", "OOP", "Functions"]
  }
]
```

**Use Case**: Display available subjects to user on home screen

---

#### 2. Start Assessment

```http
POST /api/assessment/start?subject=Python&user_id=user123
```

**Parameters:**
- `subject` (required): Subject name (e.g., "Python")
- `user_id` (optional): User identifier for tracking

**Response:**
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "subject": "Python",
  "is_active": true,
  "total_questions": 15,
  "questions_answered": 0,
  "created_at": "2025-10-03T10:00:00Z"
}
```

**Use Case**: Initialize assessment session, store `session_id` for subsequent requests

---

#### 3. Get Next Question

```http
POST /api/assessment/next-question
Content-Type: application/json

{
  "session_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Response:**
```json
{
  "question": {
    "_id": "q123",
    "question": "What is a list in Python?",
    "option_a": "A mutable ordered sequence",
    "option_b": "An immutable sequence",
    "option_c": "A key-value pair collection",
    "option_d": "A set of unique values",
    "difficulty": "easy",
    "subject": "Python",
    "topic": "Data Structures"
  },
  "question_number": 1,
  "total_questions": 15,
  "can_request_more": true
}
```

**Use Case**: Display question to user. The API automatically adapts difficulty based on BKT mastery scores.

**Important**: Store `question._id` for answer submission

---

#### 4. Submit Answer

```http
POST /api/assessment/submit-answer
Content-Type: application/json

{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "question_id": "q123",
  "selected_answer": "A",
  "time_taken_seconds": 15
}
```

**Request Body:**
- `session_id` (required): Current session ID
- `question_id` (required): Question ID from previous response
- `selected_answer` (required): User's selected option ("A", "B", "C", or "D")
- `time_taken_seconds` (optional): Time taken to answer

**Response:**
```json
{
  "success": true,
  "is_correct": true,
  "correct_answer": "A",
  "topic": "Data Structures"
}
```

**Use Case**: Submit user's answer and get immediate feedback. BKT model updates mastery in background.

---

#### 5. Complete Assessment

```http
POST /api/assessment/complete?session_id=550e8400-e29b-41d4-a716-446655440000
```

**Response:**
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "total_answered": 15,
  "score": 80.0,
  "message": "Assessment completed. Score: 80.0%"
}
```

**Use Case**: Mark assessment as complete, get final score

---

#### 6. Get Learning Path

```http
GET /api/learning-path/550e8400-e29b-41d4-a716-446655440000
```

**Response:**
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "subject": "Python",
  "overall_score": 0.75,
  "mastery_by_topic": {
    "Data Structures": 0.85,
    "OOP": 0.45,
    "Functions": 0.70
  },
  "weak_topics": [
    {
      "topic": "OOP",
      "mastery_score": 0.45,
      "priority": "high",
      "recommended_difficulty": "easy",
      "questions_to_practice": 10
    }
  ],
  "strong_topics": ["Data Structures", "Functions"],
  "recommended_course_outline": [
    "Review and strengthen weak topics: OOP",
    "Practice with adaptive difficulty questions",
    "Focus on understanding core concepts",
    "Advanced topics to explore: Data Structures, Functions"
  ],
  "generated_at": "2025-10-03T10:15:00Z"
}
```

**Use Case**: Display personalized learning path with weak areas highlighted

---

### Error Handling

All endpoints return standard HTTP status codes:

- `200 OK` - Success
- `400 Bad Request` - Invalid request (e.g., assessment already completed)
- `403 Forbidden` - Invalid API key (admin routes)
- `404 Not Found` - Resource not found (e.g., invalid session_id)

**Error Response Format:**
```json
{
  "detail": "Session not found"
}
```

---

### Frontend Implementation Example (React/TypeScript)

```typescript
// 1. Start assessment
const startAssessment = async (subject: string) => {
  const response = await fetch(`/api/assessment/start?subject=${subject}`, {
    method: 'POST'
  });
  const data = await response.json();
  return data.session_id;
};

// 2. Get next question
const getNextQuestion = async (sessionId: string) => {
  const response = await fetch('/api/assessment/next-question', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ session_id: sessionId })
  });
  return await response.json();
};

// 3. Submit answer
const submitAnswer = async (sessionId: string, questionId: string, answer: string) => {
  const response = await fetch('/api/assessment/submit-answer', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      session_id: sessionId,
      question_id: questionId,
      selected_answer: answer
    })
  });
  return await response.json();
};

// 4. Complete and get learning path
const completeAndGetPath = async (sessionId: string) => {
  await fetch(`/api/assessment/complete?session_id=${sessionId}`, {
    method: 'POST'
  });
  
  const response = await fetch(`/api/learning-path/${sessionId}`);
  return await response.json();
};
```

---

## For AI/ML Team

### BKT Model Integration

The backend implements **Bayesian Knowledge Tracing (BKT)** to track user knowledge state and adapt question difficulty.

#### BKT Parameters

```python
p_init = 0.1      # Initial mastery probability
p_learn = 0.3     # Probability of learning per attempt
p_slip = 0.1      # Probability of slip (knows but answers wrong)
p_guess = 0.25    # Probability of guess (doesn't know but answers right)
```

#### Mastery Update Formula

After each answer submission:

```
P(mastery_new | correct) = P(mastery) * P(correct | mastery) / P(correct)

where:
- P(correct | mastery) = 1 - p_slip
- P(correct | not mastery) = p_guess
```

#### Difficulty Recommendation

```python
if mastery < 0.3:
    recommend "easy"
elif mastery < 0.6:
    recommend "medium"
else:
    recommend "hard"
```

### ML Model Integration Endpoint

```http
POST /api/ai/ingest
X-API-Key: <AI_API_KEY>
Content-Type: application/json

{
  "session_id": "...",
  "user_performance": {...},
  "model_predictions": {...}
}
```

**Purpose**: This endpoint is designed for ML model integration. Currently it's a mock endpoint that returns success.

**Future Integration**: 
- Replace mock with real model inference
- Use for personalized course generation
- Feed learning path recommendations
- Power advanced analytics

### Data Schema for ML Analytics

#### User Skills Collection

```json
{
  "_id": "skill123",
  "session_id": "session456",
  "user_id": "user789",
  "subject": "Python",
  "topic": "OOP",
  "mastery_probability": 0.65,
  "attempts_count": 5,
  "correct_count": 3,
  "last_updated": "2025-10-03T10:15:00Z"
}
```

#### Attempts Collection

```json
{
  "_id": "attempt123",
  "session_id": "session456",
  "question_id": "q789",
  "selected_answer": "B",
  "correct_answer": "A",
  "is_correct": false,
  "difficulty": "medium",
  "topic": "Data Structures",
  "time_taken_seconds": 25,
  "answered_at": "2025-10-03T10:10:00Z"
}
```

### Admin Endpoints for Data Management

#### Add Single Question

```http
POST /api/admin/questions
X-API-Key: <ADMIN_API_KEY>
Content-Type: application/json

{
  "question": "What is polymorphism?",
  "option_a": "Many forms",
  "option_b": "Single form",
  "option_c": "No form",
  "option_d": "Abstract form",
  "correct_answer": "A",
  "difficulty": "hard",
  "subject": "Python",
  "topic": "OOP"
}
```

#### Bulk Add Questions

```http
POST /api/admin/questions/bulk
X-API-Key: <ADMIN_API_KEY>
Content-Type: application/json

[
  { "question": "...", ... },
  { "question": "...", ... }
]
```

**Response:**
```json
{
  "success": true,
  "inserted_count": 10,
  "inserted_ids": ["id1", "id2", ...]
}
```

#### Get All Sessions

```http
GET /api/admin/sessions
X-API-Key: <ADMIN_API_KEY>
```

#### Get Session Analytics

```http
GET /api/admin/analytics/{session_id}
X-API-Key: <ADMIN_API_KEY>
```

**Response:**
```json
{
  "session": { ... },
  "attempts": [ ... ],
  "user_skills": [ ... ],
  "total_attempts": 15,
  "correct_attempts": 12
}
```

**Use Case**: Export data for Power BI, model training, or analytics dashboards

---

## Database Collections

### questions
- **Fields**: question, option_a, option_b, option_c, option_d, correct_answer, difficulty, subject, topic
- **Purpose**: Question bank for assessments

### sessions
- **Fields**: session_id, user_id, subject, created_at, completed_at, is_active, total_questions, questions_answered
- **Purpose**: Track assessment sessions

### attempts
- **Fields**: session_id, question_id, selected_answer, correct_answer, is_correct, difficulty, topic, time_taken_seconds, answered_at
- **Purpose**: Record all answer attempts for analytics

### user_skills
- **Fields**: session_id, user_id, subject, topic, mastery_probability, attempts_count, correct_count, last_updated
- **Purpose**: Store BKT mastery scores per topic

---

## Environment Configuration

Create a `.env` file:

```bash
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=adaptive_learning
USE_IN_MEMORY=false

ADMIN_API_KEY=your-secure-admin-key
AI_API_KEY=your-secure-ai-key

CORS_ORIGINS=["http://localhost:3000"]
```

**Note**: If `MONGODB_URL` is not set or `USE_IN_MEMORY=true`, the system uses in-memory storage (data persists only during runtime).

---

## Running the Backend

### Setup

```bash
# Install dependencies (done automatically in Replit)
pip install -r requirements.txt

# Seed the database
python seed_data.py

# Run the server
uvicorn app.main:app --host 0.0.0.0 --port 5000 --reload
```

### Testing

```bash
# Run tests
pytest tests/

# Run specific test file
pytest tests/test_api.py -v
```

### Interactive API Documentation

Once running, visit:
- Swagger UI: `http://localhost:5000/docs`
- ReDoc: `http://localhost:5000/redoc`

---

## Power BI Integration

### Data Export Endpoints

Use admin endpoints to export data:

1. **Sessions**: `GET /api/admin/sessions`
2. **Analytics**: `GET /api/admin/analytics/{session_id}`

### Metrics to Track

- Overall success rate by subject
- Topic-wise mastery distribution
- Question difficulty vs. success rate
- Average time per question
- Learning progression over time
- User engagement metrics

---

## Security Notes

- **API Keys**: Change default keys in production
- **CORS**: Update `CORS_ORIGINS` for production domains
- **Database**: Use MongoDB with proper authentication in production
- **Rate Limiting**: Consider adding rate limiting for production

---

## Support

For questions or issues:
- Backend Team: Check logs in `/tmp/logs/`
- API Documentation: `/docs` endpoint
- Database: Currently using in-memory storage (check `.env` for MongoDB config)
