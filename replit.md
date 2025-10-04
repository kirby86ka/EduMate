# Adaptive Learning API

## Overview

This is a FastAPI-based adaptive learning backend that implements Bayesian Knowledge Tracing (BKT) to personalize educational assessments. The system dynamically adjusts question difficulty based on real-time user performance, tracking mastery levels across different subjects and topics to provide personalized learning paths.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Core Technology Stack
- **Backend Framework**: FastAPI (Python) with async/await for high-performance API endpoints
- **AI Engine**: Google Gemini 2.5 Flash for dynamic question generation
  - Real-time question generation based on subject, topic, and difficulty
  - Structured JSON output for consistent question format
  - Adaptive difficulty progression using BKT model
- **Storage**: In-memory storage for session tracking and user progress
  - Fast performance for real-time assessments
  - Session management with UUID-based IDs
  - User skill tracking per topic/subject
- **API Documentation**: Auto-generated OpenAPI/Swagger docs via FastAPI
- **CORS**: Configured to allow all hosts for Replit deployment

### Authentication & Security
- **API Key Authentication**: Two-tier system using header-based keys
  - Admin API Key: For administrative operations (question management, bulk operations)
  - AI API Key: For AI agent integration endpoints
  - Implementation: FastAPI Security dependencies with APIKeyHeader
  - Keys configurable via environment variables with insecure defaults for development

### Adaptive Learning Engine (BKT)
- **Bayesian Knowledge Tracing Model**: Core algorithm for mastery estimation
  - Parameters: p_learn (learning rate), p_slip (slip probability), p_guess (guess probability)
  - Updates user mastery probability after each question attempt
  - Difficulty recommendation based on mastery thresholds:
    - < 30%: Easy questions
    - 30-60%: Medium questions  
    - > 60%: Hard questions
- **Session-based Tracking**: Each assessment creates a unique session tracking:
  - Question attempts with correctness
  - Time spent per question
  - Topic-level skill progression
  - Overall performance metrics

### Data Models
- **Question**: Multi-choice questions with difficulty levels (easy/medium/hard), subject, and topic classification
- **AssessmentSession**: Tracks user progress through assessment lifecycle
- **Attempt**: Records individual question responses with timing
- **UserSkill**: Maintains mastery levels per topic/subject combination
- **LearningPath**: Generated recommendations based on skill gaps

### API Architecture
- **RESTful Design**: Resource-oriented endpoints
- **Assessment Flow**:
  1. GET /api/subjects - Retrieve available subjects
  2. POST /api/assessment/start - Initialize session with subject
  3. POST /api/assessment/next-question - BKT-driven question selection
  4. POST /api/assessment/submit-answer - Process response, update mastery
  5. POST /api/assessment/complete - Finalize and get learning path
- **Admin Routes**: Protected CRUD operations for question management
- **AI Integration Routes**: Endpoints for AI agents to interact with system

### Storage Design
- **In-Memory Storage**:
  - `sessions`: Active and historical assessment sessions with UUID keys
  - `attempts`: Question attempt history linked to sessions
  - `user_skills`: Mastery tracking per user/topic/subject
  - `question_history`: Track asked questions to avoid duplicates
- **Data Persistence**: All data stored in-memory during runtime (resets on restart)
- **ID Strategy**: UUID-based session and attempt IDs

### Configuration Management
- **Environment-based Settings**: Pydantic Settings for type-safe configuration
- **Key Configurations**:
  - Firebase service account credentials (JSON file path)
  - API keys for authentication
  - CORS origins for frontend integration
  - Application metadata

### Analytics & Reporting
- **Power BI Integration**: Dedicated endpoint (`/api/powerbi/analytics`) providing:
  - Overall performance metrics (total sessions, attempts, accuracy)
  - Subject-level performance analysis
  - Topic-wise mastery scores and learner distribution
  - Difficulty-based success rates
  - Time-series data for temporal analysis
  - Aggregated data ready for Power BI dashboard consumption

## External Dependencies

### Required Services
- **Google Gemini AI**: LLM service for question generation
  - Requires Gemini API key from Google AI Studio
  - Uses gemini-2.5-flash model for fast question generation
  - Structured JSON output with Pydantic validation

### Python Packages
- **FastAPI**: Web framework for building APIs
- **google-genai**: Official Google Gemini SDK for Python
- **Pydantic**: Data validation and settings management
- **Pydantic-settings**: Environment variable configuration
- **Uvicorn**: ASGI server for running FastAPI

### Development/Testing
- **Pytest**: Testing framework
- **HTTPX**: Async HTTP client for API testing
- **Python-dotenv**: Environment variable loading from .env files

### Frontend Application
- **Framework**: React 19 with Vite and React Router
- **UI Library**: shadcn/ui components with Tailwind CSS
- **Port**: Runs on port 5000 (Replit webview requirement)
- **Pages**:
  - **Home**: Welcome page with three action cards (Adaptive Learning, Skill Mastery, Personalized Path)
  - **Subjects**: Choose from Maths, Science, or Python to start a quiz
  - **Quiz**: Interactive assessment with real-time feedback and difficulty adaptation
  - **Dashboard**: Power BI analytics dashboard integration
  - **Personalized Path**: Gemini AI recommendations and learning resources
- **Navigation**: Clean header with Home, Subjects, and Dashboard links
- **Styling**: Modern gradient design with shadcn/ui components
- **API Integration**: Connects to FastAPI backend on port 8000
- **Location**: `/frontend` directory