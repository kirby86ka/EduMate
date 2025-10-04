const API_BASE_URL = window.location.hostname === 'localhost' 
  ? 'http://localhost:8000' 
  : `${window.location.protocol}//${window.location.hostname}:8000`;

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
}

export default new ApiService();
