import { useState, useEffect } from 'react'
import api from '../services/api'

function Assessment({ subject, sessionId, onComplete }) {
  const [question, setQuestion] = useState(null)
  const [selectedAnswer, setSelectedAnswer] = useState(null)
  const [showFeedback, setShowFeedback] = useState(false)
  const [isCorrect, setIsCorrect] = useState(false)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [questionsAnswered, setQuestionsAnswered] = useState(0)
  const [startTime, setStartTime] = useState(Date.now())
  const [finished, setFinished] = useState(false)

  useEffect(() => {
    loadNextQuestion()
  }, [])

  const loadNextQuestion = async () => {
    try {
      setLoading(true)
      setError(null)
      setSelectedAnswer(null)
      setShowFeedback(false)
      setStartTime(Date.now())
      
      const response = await api.getNextQuestion(sessionId)
      
      if (response.finished) {
        setFinished(true)
        setLoading(false)
        return
      }
      
      setQuestion(response.question)
      setLoading(false)
    } catch (err) {
      setError('Failed to load next question. Please try again.')
      console.error('Error loading question:', err)
      setLoading(false)
    }
  }

  const handleAnswerSelect = (answer) => {
    if (!showFeedback) {
      setSelectedAnswer(answer)
    }
  }

  const handleSubmit = async () => {
    if (!selectedAnswer || showFeedback) return

    try {
      const timeTaken = Math.floor((Date.now() - startTime) / 1000)
      const response = await api.submitAnswer(
        sessionId,
        question.id,
        selectedAnswer,
        timeTaken
      )

      setIsCorrect(response.is_correct)
      setShowFeedback(true)
      setQuestionsAnswered(prev => prev + 1)
    } catch (err) {
      setError('Failed to submit answer. Please try again.')
      console.error('Error submitting answer:', err)
    }
  }

  const handleNext = () => {
    loadNextQuestion()
  }

  const handleFinish = async () => {
    try {
      await api.completeAssessment(sessionId)
      onComplete()
    } catch (err) {
      setError('Failed to complete assessment. Please try again.')
      console.error('Error completing assessment:', err)
    }
  }

  if (loading) {
    return (
      <div className="card">
        <div className="loading">Loading question...</div>
      </div>
    )
  }

  if (finished) {
    return (
      <div className="card">
        <h2>Assessment Complete!</h2>
        <p>You have answered {questionsAnswered} questions.</p>
        <p>Click below to see your results and personalized learning path.</p>
        <div className="button-group">
          <button onClick={handleFinish}>View Results</button>
        </div>
      </div>
    )
  }

  if (!question) {
    return (
      <div className="card">
        {error ? (
          <div className="error">{error}</div>
        ) : (
          <div className="loading">No questions available</div>
        )}
      </div>
    )
  }

  return (
    <div className="card">
      <div style={{ marginBottom: '20px' }}>
        <div className="info-badge">{subject}</div>
        <div className="info-badge">Question {questionsAnswered + 1}</div>
        <div className="info-badge">Difficulty: {question.difficulty}</div>
      </div>

      {error && <div className="error">{error}</div>}

      <div className="question-container">
        <div className="question-text">{question.question}</div>

        <div className="options-grid">
          {['A', 'B', 'C', 'D'].map((option) => {
            const optionKey = `option_${option.toLowerCase()}`
            const optionText = question[optionKey]
            
            if (!optionText) return null

            let className = 'option-button'
            if (selectedAnswer === option) {
              className += ' selected'
            }
            if (showFeedback) {
              if (option === question.correct_answer) {
                className += ' correct'
              } else if (option === selectedAnswer && !isCorrect) {
                className += ' incorrect'
              }
            }

            return (
              <button
                key={option}
                className={className}
                onClick={() => handleAnswerSelect(option)}
                disabled={showFeedback}
              >
                <strong>{option}.</strong> {optionText}
              </button>
            )
          })}
        </div>

        {showFeedback && (
          <div className={`feedback ${isCorrect ? 'correct' : 'incorrect'}`}>
            {isCorrect ? (
              <strong>Correct!</strong>
            ) : (
              <>
                <strong>Incorrect.</strong> The correct answer was{' '}
                <strong>{question.correct_answer}</strong>.
              </>
            )}
          </div>
        )}

        <div className="button-group">
          {!showFeedback ? (
            <button onClick={handleSubmit} disabled={!selectedAnswer}>
              Submit Answer
            </button>
          ) : (
            <button onClick={handleNext}>Next Question</button>
          )}
        </div>
      </div>
    </div>
  )
}

export default Assessment
