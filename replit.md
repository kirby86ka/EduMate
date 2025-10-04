# Adaptive Learning API

## Overview

This is a FastAPI-based adaptive learning backend that implements Bayesian Knowledge Tracing (BKT) to personalize educational assessments. The system dynamically adjusts question difficulty based on real-time user performance, tracking mastery levels across different subjects and topics to provide personalized learning paths.

## User Preferences

Preferred communication style: Simple, everyday language.

## Documentation

Complete documentation available in:
- **README.md**: Comprehensive project overview, installation, API docs, and deployment guide
- **CONTRIBUTING.md**: Guidelines for contributing to the project
- **LICENSE**: MIT License

## System Architecture

### Core Technology Stack
- **Backend Framework**: FastAPI (Python) with async/await for high-performance API endpoints
- **AI Engine**: Google Gemini 2.5 Flash for dynamic question generation
  - Real-time question generation based on subject, topic, and difficulty
  - Structured JSON output for consistent question format
  - Adaptive difficulty progression using BKT model
  - 15-second timeout protection with thread pool execution
  - Max 500 output tokens for faster response times
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
  3. POST /api/assessment/next-question - BKT-driven question selection (20s frontend timeout, 15s backend Gemini timeout)
  4. POST /api/assessment/submit-answer - Process response, update mastery (10s frontend timeout)
  5. POST /api/assessment/complete - Finalize and get learning path
- **Admin Routes**: Protected CRUD operations for question management
- **AI Integration Routes**: Endpoints for AI agents to interact with system
- **Timeout Handling**: Frontend uses AbortController for request timeouts with user-friendly error messages

### Storage Design
- **In-Memory Storage**:
  - `sessions`: Active and historical assessment sessions with UUID keys
  - `attempts`: Question attempt history linked to sessions
  - `user_skills`: Mastery tracking per user/topic/subject
  - `question_history`: Track asked questions to avoid duplicates
  - `current_questions`: Stores complete question payloads for answer validation
- **Data Persistence**: All data stored in-memory during runtime (resets on restart)
- **ID Strategy**: UUID-based session and attempt IDs
- **Question Lifecycle**: Questions are generated → stored → validated → cleared after submission to ensure accurate BKT updates

### Configuration Management
- **Environment-based Settings**: Pydantic Settings for type-safe configuration
- **Key Configurations**:
  - Gemini API key for AI question generation
  - API keys for authentication
  - CORS origins for frontend integration
  - Application metadata

### Analytics & Reporting
- **Custom Analytics Dashboard**: Built with shadcn/ui components and Recharts visualization
  - Subject-specific analytics via `/api/analytics/subject/{subject}` endpoint
  - Three subject tabs (Maths, Science, Python) with lazy-loading data
  - Growth charts showing accuracy progression over question attempts
  - Question history with topics, difficulty levels, and results
  - Bayesian mastery estimates with color-coded proficiency indicators (Proficient ≥70%, Developing ≥40%, Beginner <40%)
  - Real-time data aggregation from assessment sessions and attempts
  - Empty state handling for subjects with no quiz data
- **Legacy Power BI endpoint**: `/api/powerbi/analytics` still available for external integrations

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
- **Charting**: Recharts for data visualization
- **Markdown/LaTeX**: react-markdown with remark-math, remark-gfm, and rehype-katex for rendering AI content
- **Port**: Runs on port 5000 (Replit webview requirement)
- **Theme**: Dark theme with white text on black background using CSS custom properties
  - Background: Pure black (#000000)
  - Foreground text: White (#FFFFFF)
  - Muted text: Gray (#A1A1AA)
  - Logo: Bright yellow (#F5C211) with pulsing brain icon
  - Accent colors: Purple primary, green/red for correctness indicators
  - Consistent use of `bg-background`, `text-foreground`, `border-border` classes
- **Animations & Transitions**: Smooth CSS animations throughout the site
  - Keyframe animations: fadeIn, slideUp, slideIn, scaleIn with staggered delays
  - Hover effects: lift animation on cards, scale on buttons, rotate on icons
  - Navigation: active link underline animation with yellow highlight
  - Transition utilities: smooth easing with cubic-bezier curves
- **Responsive Design**: Mobile-first approach with Tailwind breakpoints
  - xs (extra small): < 640px - Mobile phones
  - sm (small): 640px+ - Large phones, small tablets
  - md (medium): 768px+ - Tablets, small laptops
  - Responsive text sizes, spacing, and grid layouts across all pages
- **Performance Optimizations**:
  - React.lazy for route-level code splitting
  - Suspense with branded loading fallback
  - React.memo for component memoization
  - Optimized re-renders and bundle sizes
- **Pages**:
  - **Home**: Welcome page with three action cards (Adaptive Learning, Skill Mastery, Personalized Path)
    - Brain icon in navigation header next to AdaptLearn logo
    - Last Quiz Results section showing recent quiz performance with link to Dashboard
    - Backend endpoint: `/api/learning-path/last-quiz`
  - **Subjects**: Choose from Maths, Science, or Python to start a quiz
  - **Quiz**: Interactive 10-question assessment with real-time feedback and difficulty adaptation
    - Detailed results screen with score (X/10), percentage, and question-by-question breakdown
    - Green/red color coding for correct/incorrect answers
    - Topics displayed for each question
  - **Dashboard**: Custom analytics dashboard with subject-specific views
    - Tabbed interface for Maths, Science, and Python
    - Growth chart showing accuracy trends over questions
    - Question history with topics and difficulty levels
    - Bayesian mastery estimate with color-coded proficiency levels
  - **Personalized Path**: Subject-specific AI-powered learning recommendations
    - Tabbed interface for Maths, Science, and Python
    - Markdown and LaTeX rendering for AI-generated content
    - Backend endpoint: `/api/learning-path/recommendations/{subject}`
    - Displays personalized study materials, topics to review, and resource links
- **Navigation**: Clean header with brain icon, AdaptLearn logo, Home, Subjects, and Dashboard links
- **Styling**: Dark theme with shadcn/ui components and consistent color palette
- **API Integration**: Connects to FastAPI backend on port 8000
- **Location**: `/frontend` directory

## Deployment

### Replit Deployment (Current)
- **Autoscale Deployment**: Single-port architecture with FastAPI serving both API and static frontend
  - `.replit`: Main configuration file for deployment and workflows
  - FastAPI serves React build from `frontend/dist` on port 8000
  - Auto-deployment on file changes
  - Environment secrets managed in Replit dashboard
- **Features**:
  - Built-in scaling based on traffic
  - Free SSL certificates
  - Custom domain support
  - Automatic HTTPS
  - Zero-downtime deployments
- **Setup**: Click "Deploy" button in Replit, configure environment secrets
- **Environment**: Requires GEMINI_API_KEY and SESSION_SECRET