# 🧠 AdaptLearn - Adaptive Learning Platform

An intelligent educational platform that personalizes assessments using **Bayesian Knowledge Tracing (BKT)** and **AI-powered question generation**. The system dynamically adjusts question difficulty based on real-time performance, providing personalized learning paths for students.

![Platform Demo](https://img.shields.io/badge/Status-Production%20Ready-green)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![React](https://img.shields.io/badge/React-19-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688)

## ✨ Features

### 🎯 Adaptive Assessment Engine
- **Bayesian Knowledge Tracing (BKT)**: Real-time mastery estimation
- **Dynamic Difficulty Adjustment**: Questions adapt based on performance
- **AI Question Generation**: Powered by Google Gemini 2.5 Flash
- **LaTeX & Markdown Support**: Beautiful rendering of math equations and code

### 📊 Analytics & Insights
- **Subject-Specific Dashboards**: Track progress across Maths, Science, and Python
- **Growth Charts**: Visualize accuracy trends over time
- **Mastery Estimates**: Bayesian-based proficiency tracking with color-coded levels
- **Question History**: Complete breakdown of topics and difficulty

### 🎓 Personalized Learning
- **AI-Powered Recommendations**: Custom study plans based on performance
- **Learning Path Generation**: Targeted resource suggestions
- **Topic-Level Tracking**: Granular skill monitoring across subjects

### 🎨 Modern UI/UX
- **Dark Theme**: Eye-friendly design with yellow branding
- **Responsive Design**: Mobile-first approach for all devices
- **Smooth Animations**: Fluid transitions and hover effects
- **Code Splitting**: Optimized loading with React.lazy

## 🏗️ Architecture

### Backend
- **Framework**: FastAPI (Python) with async/await
- **AI Engine**: Google Gemini 2.5 Flash
  - 15-second timeout protection
  - Thread pool execution for non-blocking operations
  - Max 500 output tokens for fast generation
- **Storage**: In-memory storage with session management
- **Authentication**: Two-tier API key system (Admin & AI)

### Frontend
- **Framework**: React 19 with Vite
- **UI Library**: shadcn/ui components
- **Styling**: Tailwind CSS with custom dark theme
- **Charting**: Recharts for data visualization
- **Math Rendering**: KaTeX with react-markdown
- **Routing**: React Router for SPA navigation

### Adaptive Learning Flow
```
User Starts Quiz
    ↓
Initialize Session (BKT: 50% mastery)
    ↓
Generate Question (AI + Difficulty)
    ↓
User Answers
    ↓
Update Mastery (BKT Algorithm)
    ↓
Recommend Next Difficulty
    ↓
[Repeat for 10 questions]
    ↓
Generate Learning Path
```

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Node.js 20+
- Google Gemini API Key ([Get one here](https://aistudio.google.com/app/apikey))

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/adaptlearn.git
cd adaptlearn
```

2. **Set up environment variables**
```bash
cp .env.example .env
```

Edit `.env` and add your Gemini API key:
```env
GEMINI_API_KEY=your_api_key_here
SESSION_SECRET=your_random_secret_here
```

3. **Install backend dependencies**
```bash
pip install -r requirements.txt
```

4. **Install frontend dependencies**
```bash
cd frontend
npm install
cd ..
```

5. **Run the application**

**Development Mode:**
```bash
# Terminal 1 - Backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2 - Frontend
cd frontend
npm run dev
```

**Production Mode (Single Server):**
```bash
# Build frontend
cd frontend
npm run build
cd ..

# Serve both from FastAPI
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Visit `http://localhost:5000` (dev) or `http://localhost:8000` (prod)

## 📚 API Documentation

### Core Endpoints

#### Start Assessment
```http
POST /api/assessment/start?subject=Maths
```
**Response:**
```json
{
  "session_id": "uuid",
  "subject": "Maths",
  "status": "active",
  "mastery_level": 0.5
}
```

#### Get Next Question
```http
POST /api/assessment/next-question
Content-Type: application/json

{
  "session_id": "uuid"
}
```

**Response:**
```json
{
  "question": "What is $x^2 + 2x + 1$?",
  "option_a": "$(x+1)^2$",
  "option_b": "$(x-1)^2$",
  "option_c": "$x^2 + 1$",
  "option_d": "$2x^2$",
  "topic": "Algebra",
  "current_difficulty": "medium"
}
```

#### Submit Answer
```http
POST /api/assessment/submit-answer
Content-Type: application/json

{
  "session_id": "uuid",
  "selected_answer": "A",
  "time_spent": 15,
  "topic": "Algebra"
}
```

**Response:**
```json
{
  "is_correct": true,
  "correct_answer": "A",
  "explanation": "$(x+1)^2 = x^2 + 2x + 1$",
  "new_mastery": 0.65
}
```

#### Complete Assessment
```http
POST /api/assessment/complete?session_id=uuid
```

### Analytics Endpoints

#### Subject Analytics
```http
GET /api/analytics/subject/Maths
```

#### Learning Recommendations
```http
GET /api/learning-path/recommendations?subject=Maths
```

Full API documentation available at `/docs` (Swagger UI)

## 🎓 Bayesian Knowledge Tracing (BKT)

The platform uses BKT to estimate user mastery in real-time:

### Parameters
- **p_learn**: 0.3 (probability of learning from correct answer)
- **p_slip**: 0.1 (probability of making a mistake despite knowing)
- **p_guess**: 0.25 (probability of guessing correctly)

### Update Formula
```python
if correct:
    new_mastery = mastery + (1 - mastery) * p_learn
else:
    new_mastery = mastery * (1 - p_slip)
```

### Difficulty Mapping
- **< 30% mastery** → Easy questions
- **30-60% mastery** → Medium questions  
- **> 60% mastery** → Hard questions

## 🎨 UI Components

### Subjects
- 🔢 **Maths**: Arithmetic, Algebra, Geometry, Calculus
- 🔬 **Science**: Physics, Chemistry, Biology, Earth Science
- 🐍 **Python**: Basics, Data Structures, OOP, Advanced Concepts

### Pages
- **Home**: Welcome screen with last quiz results
- **Subjects**: Choose quiz subject
- **Quiz**: 10-question adaptive assessment with real-time feedback
- **Dashboard**: Analytics with subject-specific tabs
- **Personalized Path**: AI-generated learning recommendations

## 🐳 Deployment

### Docker
```bash
docker-compose up -d
```

Services:
- Backend: `http://localhost:8000`
- Frontend: `http://localhost:5000`

### Vercel (Recommended)
1. Connect GitHub repo to Vercel
2. Add environment variables in Vercel dashboard:
   - `GEMINI_API_KEY`
   - `SESSION_SECRET`
3. Deploy automatically on push

See [VERCEL_DEPLOY.md](VERCEL_DEPLOY.md) for detailed instructions.

### Replit (Autoscale)
Configured with `.replit` for single-port architecture:
- FastAPI serves both API and static frontend
- Auto-deployment on file changes
- Environment secrets managed in Replit dashboard

## 📁 Project Structure

```
adaptlearn/
├── app/                        # Backend (FastAPI)
│   ├── main.py                # API routes & server
│   ├── models/                # Pydantic models
│   │   └── schemas.py
│   └── services/              # Business logic
│       ├── bkt_model.py       # Bayesian Knowledge Tracing
│       ├── question_generator.py  # AI question generation
│       └── storage.py         # In-memory data store
├── frontend/                   # Frontend (React)
│   ├── src/
│   │   ├── components/        # UI components
│   │   │   └── ui/           # shadcn/ui components
│   │   ├── pages/            # Route pages
│   │   │   ├── Home.jsx
│   │   │   ├── Subjects.jsx
│   │   │   ├── Quiz.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   └── PersonalizedPath.jsx
│   │   ├── services/         # API client
│   │   │   └── api.js
│   │   └── styles/           # Global styles
│   ├── package.json
│   └── vite.config.js
├── api/                       # Vercel serverless
│   └── index.py
├── .replit                    # Replit configuration
├── docker-compose.yml         # Docker setup
├── Dockerfile                 # Multi-stage build
├── requirements.txt           # Python dependencies
└── README.md
```

## 🔧 Configuration

### Environment Variables
```env
# Required
GEMINI_API_KEY=your_gemini_api_key
SESSION_SECRET=your_random_secret

# Optional (Development)
ADMIN_API_KEY=dev-admin-key-12345
AI_API_KEY=dev-ai-key-67890
```

### Timeout Settings
- **Backend Gemini**: 15 seconds
- **Frontend Question Fetch**: 20 seconds
- **Frontend Answer Submit**: 10 seconds

## 🧪 Testing

```bash
# Backend tests
pytest

# Frontend tests
cd frontend
npm test
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style
- **Python**: Follow PEP 8
- **JavaScript**: ESLint configuration included
- **Commits**: Use conventional commits format

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Gemini**: AI-powered question generation
- **shadcn/ui**: Beautiful UI components
- **Recharts**: Data visualization
- **KaTeX**: Math rendering
- **FastAPI**: High-performance backend framework

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Built with ❤️ using FastAPI, React, and AI**
