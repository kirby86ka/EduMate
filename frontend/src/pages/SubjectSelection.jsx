import { useState, useEffect } from 'react'
import api from '../services/api'

function SubjectSelection({ onSubjectSelect }) {
  const [subjects, setSubjects] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    loadSubjects()
  }, [])

  const loadSubjects = async () => {
    try {
      setLoading(true)
      setError(null)
      const data = await api.getSubjects()
      setSubjects(data)
    } catch (err) {
      setError('Unable to load subjects. Please make sure the backend server is running.')
      console.error('Error loading subjects:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleSubjectClick = async (subject) => {
    try {
      setError(null)
      const session = await api.startAssessment(subject.subject)
      onSubjectSelect(subject.subject, session)
    } catch (err) {
      setError(`Failed to start assessment for ${subject.subject}. Please try again.`)
      console.error('Error starting assessment:', err)
    }
  }

  if (loading) {
    return (
      <div className="card">
        <div className="loading">Loading subjects...</div>
      </div>
    )
  }

  return (
    <div className="card">
      <h1>Adaptive Learning Platform</h1>
      <p className="subtitle">
        Choose a subject to begin your personalized assessment
      </p>

      {error && (
        <div className="error">
          {error}
        </div>
      )}

      {subjects.length === 0 && !error && (
        <div className="error">
          No subjects available. Please seed the database with questions using the backend seed script.
        </div>
      )}

      <div className="subject-grid">
        {subjects.map((subject) => (
          <div
            key={subject.subject}
            className="subject-card"
            onClick={() => handleSubjectClick(subject)}
          >
            <h3>{subject.subject}</h3>
            <p>{subject.question_count} questions</p>
            <p>{subject.topics.length} topics</p>
          </div>
        ))}
      </div>

      <p style={{ textAlign: 'center', marginTop: '30px', fontSize: '0.9rem' }}>
        The system uses Bayesian Knowledge Tracing to adapt question difficulty based on your performance.
      </p>
    </div>
  )
}

export default SubjectSelection
