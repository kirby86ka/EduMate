# Adaptive Learning API

## Overview

This is a FastAPI-based adaptive learning backend that implements Bayesian Knowledge Tracing (BKT) to personalize educational assessments. The system dynamically adjusts question difficulty based on real-time user performance, tracking mastery levels across different subjects and topics to provide personalized learning paths.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Core Technology Stack
- **Backend Framework**: FastAPI (Python) with async/await for high-performance API endpoints
- **Database Strategy**: Dual-mode storage system
  - Primary: MongoDB with Motor async driver for production scalability
  - Fallback: In-memory collections for development/testing without external dependencies
  - Rationale: Allows rapid development and testing while maintaining production-ready MongoDB integration
- **API Documentation**: Auto-generated OpenAPI/Swagger docs via FastAPI
- **CORS**: Configured for `http://localhost:3000` frontend integration

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

### Database Schema Design
- **Collections**:
  - `questions`: Question bank with metadata (subject, topic, difficulty)
  - `sessions`: Active and historical assessment sessions
  - `attempts`: Question attempt history linked to sessions
  - `user_skills`: Mastery tracking per user/topic/subject
- **ID Strategy**: String-based IDs with auto-increment for in-memory, MongoDB ObjectIds for production

### Configuration Management
- **Environment-based Settings**: Pydantic Settings for type-safe configuration
- **Key Configurations**:
  - MongoDB connection URL (optional, triggers in-memory mode if absent)
  - API keys for authentication
  - CORS origins for frontend integration
  - Database name and application metadata

## External Dependencies

### Required Services
- **MongoDB** (Optional): Document database for persistent storage
  - Connection via motor async driver
  - Falls back to in-memory if unavailable
  - Collections: questions, sessions, attempts, user_skills

### Python Packages
- **FastAPI**: Web framework for building APIs
- **Motor**: Async MongoDB driver for FastAPI integration
- **Pydantic**: Data validation and settings management
- **Pydantic-settings**: Environment variable configuration
- **Uvicorn**: ASGI server for running FastAPI

### Development/Testing
- **Pytest**: Testing framework
- **HTTPX**: Async HTTP client for API testing
- **Python-dotenv**: Environment variable loading from .env files

### Frontend Integration
- Expects frontend running on `http://localhost:3000`
- CORS pre-configured for this origin
- API responses in JSON format following OpenAPI specification