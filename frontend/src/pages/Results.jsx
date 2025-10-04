import { useState, useEffect } from 'react'
import api from '../services/api'

function Results({ sessionId, onRestart }) {
  const [results, setResults] = useState(null)
  const [learningPath, setLearningPath] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    loadResults()
  }, [])

  const loadResults = async () => {
    try {
      setLoading(true)
      setError(null)
      
      const [resultsData, pathData] = await Promise.all([
        api.completeAssessment(sessionId),
        api.getLearningPath(sessionId)
      ])
      
      setResults(resultsData)
      setLearningPath(pathData)
    } catch (err) {
      setError('Failed to load results. Please try again.')
      console.error('Error loading results:', err)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="card">
        <div className="loading">Loading your results...</div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="card">
        <div className="error">{error}</div>
        <div className="button-group">
          <button onClick={onRestart}>Start New Assessment</button>
        </div>
      </div>
    )
  }

  if (!results || !learningPath) {
    return (
      <div className="card">
        <div className="error">No results available</div>
      </div>
    )
  }

  const accuracyPercent = results.total_answered > 0
    ? Math.round((results.correct_answers / results.total_answered) * 100)
    : 0

  return (
    <div className="card">
      <h1>Assessment Results</h1>
      <p className="subtitle">Here's how you performed</p>

      <div className="stats-grid">
        <div className="stat-card">
          <span className="stat-value">{results.total_answered}</span>
          <span className="stat-label">Questions</span>
        </div>
        <div className="stat-card">
          <span className="stat-value">{results.correct_answers}</span>
          <span className="stat-label">Correct</span>
        </div>
        <div className="stat-card">
          <span className="stat-value">{accuracyPercent}%</span>
          <span className="stat-label">Accuracy</span>
        </div>
      </div>

      <div className="learning-path">
        <h2>Your Personalized Learning Path</h2>
        <p style={{ marginBottom: '20px', color: '#666' }}>
          Based on your performance, here are recommended topics to focus on:
        </p>

        {learningPath.recommended_topics && learningPath.recommended_topics.length > 0 ? (
          learningPath.recommended_topics.map((topic, index) => (
            <div key={index} className="topic-item">
              <h4>{topic.topic}</h4>
              <p>
                <strong>Current Mastery:</strong> {Math.round(topic.current_mastery * 100)}%
              </p>
              <p>
                <strong>Priority:</strong> {topic.priority}
              </p>
              <p style={{ fontSize: '0.85rem', marginTop: '8px' }}>
                {topic.recommendation}
              </p>
              <div className="mastery-bar">
                <div
                  className="mastery-fill"
                  style={{ width: `${topic.current_mastery * 100}%` }}
                />
              </div>
            </div>
          ))
        ) : (
          <p style={{ color: '#666', textAlign: 'center', padding: '20px' }}>
            Great job! You've demonstrated strong mastery across all topics.
          </p>
        )}
      </div>

      <div className="button-group">
        <button onClick={onRestart}>Start New Assessment</button>
      </div>
    </div>
  )
}

export default Results
