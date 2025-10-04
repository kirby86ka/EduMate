const getApiBaseUrl = () => {
  if (window.location.hostname === 'localhost') {
    return 'http://localhost:8000';
  }
  if (window.location.hostname.includes('replit') || window.location.hostname.includes('repl.co')) {
    return `${window.location.protocol}//${window.location.hostname}:8000`;
  }
  return '';
};

const API_BASE_URL = getApiBaseUrl();

const ADMIN_API_KEY = 'dev-admin-key-12345';

const subjectMapping = {
  'maths': 'Maths',
  'science': 'Science',
  'python': 'Python',
}

class ApiService {
  async getSubjects() {
    const response = await fetch(`${API_BASE_URL}/api/subjects`);
    if (!response.ok) throw new Error('Failed to fetch subjects');
    return response.json();
  }

  async startAssessment(subject, userId = null) {
    const mappedSubject = subjectMapping[subject] || subject;
    const response = await fetch(`${API_BASE_URL}/api/assessment/start?subject=${encodeURIComponent(mappedSubject)}${userId ? `&user_id=${userId}` : ''}`, {
      method: 'POST',
    });
    if (!response.ok) throw new Error('Failed to start assessment');
    return response.json();
  }

  async getNextQuestion(sessionId) {
    const response = await fetch(`${API_BASE_URL}/api/assessment/next-question`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ session_id: sessionId }),
    });
    if (!response.ok) throw new Error('Failed to get next question');
    return response.json();
  }

  async submitAnswer(sessionId, selectedAnswer, timeTaken, topic) {
    const response = await fetch(`${API_BASE_URL}/api/assessment/submit-answer`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        session_id: sessionId,
        selected_answer: selectedAnswer,
        time_spent: timeTaken,
        topic: topic,
      }),
    });
    if (!response.ok) throw new Error('Failed to submit answer');
    return response.json();
  }

  async completeAssessment(sessionId) {
    const response = await fetch(`${API_BASE_URL}/api/assessment/complete?session_id=${sessionId}`, {
      method: 'POST',
    });
    if (!response.ok) throw new Error('Failed to complete assessment');
    return response.json();
  }

  async getLearningPath(sessionId) {
    const response = await fetch(`${API_BASE_URL}/api/learning-path/${sessionId}`);
    if (!response.ok) throw new Error('Failed to get learning path');
    return response.json();
  }

  async getSubjectAnalytics(subject) {
    const mappedSubject = subjectMapping[subject] || subject;
    const response = await fetch(`${API_BASE_URL}/api/analytics/subject/${encodeURIComponent(mappedSubject)}`);
    if (!response.ok) throw new Error('Failed to get analytics');
    return response.json();
  }

  async getLearningRecommendations(userId = null, subject = null) {
    let url = `${API_BASE_URL}/api/learning-path/recommendations`;
    const params = new URLSearchParams();
    if (userId) params.append('user_id', userId);
    if (subject) params.append('subject', subject);
    if (params.toString()) url += `?${params.toString()}`;
    const response = await fetch(url);
    if (!response.ok) throw new Error('Failed to get recommendations');
    return response.json();
  }

  async getLastQuizResults(userId = null) {
    const url = userId 
      ? `${API_BASE_URL}/api/learning-path/last-quiz?user_id=${userId}`
      : `${API_BASE_URL}/api/learning-path/last-quiz`;
    const response = await fetch(url);
    if (!response.ok) throw new Error('Failed to get last quiz results');
    return response.json();
  }
}

export default new ApiService();
