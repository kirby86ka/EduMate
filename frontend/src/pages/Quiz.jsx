import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card'
import { Button } from '../components/ui/button'
import api from '../services/api'
import { CheckCircle2, XCircle } from 'lucide-react'

export default function Quiz() {
  const { subject } = useParams()
  const navigate = useNavigate()
  const [sessionId, setSessionId] = useState(null)
  const [question, setQuestion] = useState(null)
  const [selectedAnswer, setSelectedAnswer] = useState(null)
  const [showFeedback, setShowFeedback] = useState(false)
  const [isCorrect, setIsCorrect] = useState(false)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [questionsAnswered, setQuestionsAnswered] = useState(0)
  const [startTime, setStartTime] = useState(Date.now())

  useEffect(() => {
    startAssessment()
  }, [])

  const startAssessment = async () => {
    try {
      const session = await api.startAssessment(subject)
      setSessionId(session.session_id)
      loadNextQuestion(session.session_id)
    } catch (err) {
      setError('Failed to start assessment')
      setLoading(false)
    }
  }

  const loadNextQuestion = async (sid) => {
    try {
      setLoading(true)
      setSelectedAnswer(null)
      setShowFeedback(false)
      setStartTime(Date.now())
      
      const response = await api.getNextQuestion(sid || sessionId)
      
      if (response.finished) {
        await api.completeAssessment(sid || sessionId)
        navigate('/dashboard')
        return
      }
      
      setQuestion(response.question)
      setLoading(false)
    } catch (err) {
      setError('Failed to load question')
      setLoading(false)
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
      setError('Failed to submit answer')
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Card className="w-full max-w-2xl">
          <CardContent className="p-8 text-center">
            <p className="text-muted-foreground">Loading question...</p>
          </CardContent>
        </Card>
      </div>
    )
  }

  if (!question) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Card className="w-full max-w-2xl">
          <CardContent className="p-8 text-center">
            <p className="text-muted-foreground">{error || 'No questions available'}</p>
          </CardContent>
        </Card>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-blue-50 py-8">
      <div className="container mx-auto px-4">
        <div className="max-w-3xl mx-auto">
          <div className="mb-6 flex justify-between items-center">
            <div className="flex gap-2">
              <span className="px-3 py-1 bg-primary/10 text-primary rounded-full text-sm font-medium">
                {subject}
              </span>
              <span className="px-3 py-1 bg-secondary rounded-full text-sm font-medium">
                Question {questionsAnswered + 1}
              </span>
              <span className="px-3 py-1 bg-accent rounded-full text-sm font-medium">
                {question.difficulty}
              </span>
            </div>
          </div>

          <Card>
            <CardHeader>
              <CardTitle className="text-xl">{question.question}</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              {['A', 'B', 'C', 'D'].map((option) => {
                const optionKey = `option_${option.toLowerCase()}`
                const optionText = question[optionKey]
                
                if (!optionText) return null

                let buttonVariant = "outline"
                let extraClasses = ""
                
                if (selectedAnswer === option) {
                  buttonVariant = "secondary"
                }
                
                if (showFeedback) {
                  if (option === question.correct_answer) {
                    buttonVariant = "default"
                    extraClasses = "bg-green-500 hover:bg-green-600 border-green-600"
                  } else if (option === selectedAnswer && !isCorrect) {
                    buttonVariant = "destructive"
                  }
                }

                return (
                  <Button
                    key={option}
                    variant={buttonVariant}
                    className={`w-full justify-start text-left h-auto py-4 ${extraClasses}`}
                    onClick={() => !showFeedback && setSelectedAnswer(option)}
                    disabled={showFeedback}
                  >
                    <span className="font-bold mr-3">{option}.</span>
                    <span>{optionText}</span>
                  </Button>
                )
              })}

              {showFeedback && (
                <div className={`p-4 rounded-lg flex items-center gap-3 ${
                  isCorrect ? 'bg-green-50 text-green-800' : 'bg-red-50 text-red-800'
                }`}>
                  {isCorrect ? (
                    <>
                      <CheckCircle2 className="w-5 h-5" />
                      <span className="font-medium">Correct!</span>
                    </>
                  ) : (
                    <>
                      <XCircle className="w-5 h-5" />
                      <span className="font-medium">
                        Incorrect. The correct answer was {question.correct_answer}.
                      </span>
                    </>
                  )}
                </div>
              )}

              <div className="pt-4">
                {!showFeedback ? (
                  <Button 
                    className="w-full" 
                    onClick={handleSubmit}
                    disabled={!selectedAnswer}
                  >
                    Submit Answer
                  </Button>
                ) : (
                  <Button 
                    className="w-full" 
                    onClick={() => loadNextQuestion()}
                  >
                    Next Question
                  </Button>
                )}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}
