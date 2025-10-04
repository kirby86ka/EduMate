import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card'
import { Button } from '../components/ui/button'
import api from '../services/api'
import { CheckCircle2, XCircle } from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import remarkMath from 'remark-math'
import remarkGfm from 'remark-gfm'
import rehypeKatex from 'rehype-katex'
import 'katex/dist/katex.min.css'

const TOTAL_QUESTIONS = 10

export default function Quiz() {
  const { subject } = useParams()
  const navigate = useNavigate()
  const [sessionId, setSessionId] = useState(null)
  const [question, setQuestion] = useState(null)
  const [selectedAnswer, setSelectedAnswer] = useState(null)
  const [showFeedback, setShowFeedback] = useState(false)
  const [feedback, setFeedback] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [questionsAnswered, setQuestionsAnswered] = useState(0)
  const [startTime, setStartTime] = useState(Date.now())
  const [quizComplete, setQuizComplete] = useState(false)
  const [results, setResults] = useState(null)
  const [attemptHistory, setAttemptHistory] = useState([])

  useEffect(() => {
    const startQuiz = async () => {
      try {
        const session = await api.startAssessment(subject)
        setSessionId(session.session_id)
        
        const questionData = await api.getNextQuestion(session.session_id)
        setQuestion(questionData)
        setLoading(false)
      } catch (err) {
        setError(err.message)
        setLoading(false)
      }
    }
    
    startQuiz()
  }, [subject])

  const loadNextQuestion = async () => {
    if (questionsAnswered >= TOTAL_QUESTIONS) {
      await completeQuiz()
      return
    }

    try {
      setLoading(true)
      setSelectedAnswer(null)
      setShowFeedback(false)
      setFeedback(null)
      setStartTime(Date.now())
      
      const questionData = await api.getNextQuestion(sessionId)
      setQuestion(questionData)
      setLoading(false)
    } catch (err) {
      setError(err.message)
      setLoading(false)
    }
  }

  const handleSubmit = async () => {
    if (!selectedAnswer || showFeedback) return

    try {
      const timeTaken = Math.floor((Date.now() - startTime) / 1000)
      const response = await api.submitAnswer(
        sessionId,
        selectedAnswer,
        timeTaken,
        question.topic
      )

      setFeedback(response)
      setShowFeedback(true)
      
      const newQuestionsAnswered = questionsAnswered + 1
      setQuestionsAnswered(newQuestionsAnswered)
      
      setAttemptHistory(prev => [...prev, {
        question: question.question,
        topic: question.topic,
        selected_answer: selectedAnswer,
        correct_answer: response.correct_answer,
        is_correct: response.is_correct
      }])

    } catch (err) {
      setError(err.message)
    }
  }

  const completeQuiz = async () => {
    try {
      const completionData = await api.completeAssessment(sessionId)
      setResults(completionData)
      setQuizComplete(true)
    } catch (err) {
      setError(err.message)
    }
  }

  if (error) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <Card className="w-full max-w-2xl border-border bg-card">
          <CardContent className="p-8 text-center">
            <p className="text-red-500">{error}</p>
            <Button onClick={() => navigate('/subjects')} className="mt-4">
              Back to Subjects
            </Button>
          </CardContent>
        </Card>
      </div>
    )
  }

  if (quizComplete && results) {
    const totalCorrect = attemptHistory.filter(a => a.is_correct).length
    const percentCorrect = Math.round((totalCorrect / TOTAL_QUESTIONS) * 100)

    return (
      <div className="min-h-screen bg-background py-8">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto">
            <h1 className="text-4xl font-bold text-center mb-8 text-foreground">Quiz Complete!</h1>
            
            <div className="grid md:grid-cols-2 gap-6 mb-8">
              <Card className="border-border bg-card">
                <CardContent className="p-6 text-center">
                  <div className="text-5xl font-bold text-primary mb-2">
                    {totalCorrect}/{TOTAL_QUESTIONS}
                  </div>
                  <div className="text-muted-foreground">Results</div>
                </CardContent>
              </Card>
              
              <Card className="border-border bg-card">
                <CardContent className="p-6 text-center">
                  <div className="text-5xl font-bold text-primary mb-2">
                    {percentCorrect}%
                  </div>
                  <div className="text-muted-foreground">Percent Correct</div>
                </CardContent>
              </Card>
            </div>

            <Card className="border-border bg-card">
              <CardHeader>
                <CardTitle className="text-foreground">Question Breakdown</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {attemptHistory.map((attempt, index) => (
                    <div 
                      key={index}
                      className={`p-4 rounded-lg border-2 ${
                        attempt.is_correct 
                          ? 'border-green-500/50 bg-green-500/10' 
                          : 'border-red-500/50 bg-red-500/10'
                      }`}
                    >
                      <div className="flex items-start gap-3">
                        {attempt.is_correct ? (
                          <CheckCircle2 className="w-5 h-5 text-green-500 mt-1 flex-shrink-0" />
                        ) : (
                          <XCircle className="w-5 h-5 text-red-500 mt-1 flex-shrink-0" />
                        )}
                        <div className="flex-1">
                          <div className="flex items-center gap-2 mb-2">
                            <span className="font-semibold text-foreground">Question {index + 1}</span>
                            <span className="px-2 py-1 bg-secondary rounded text-xs font-medium text-foreground">
                              {attempt.topic}
                            </span>
                          </div>
                          <div className="text-sm mb-2 text-foreground prose prose-sm prose-invert max-w-none">
                            <ReactMarkdown 
                              remarkPlugins={[remarkMath, remarkGfm]}
                              rehypePlugins={[rehypeKatex]}
                            >
                              {attempt.question}
                            </ReactMarkdown>
                          </div>
                          <div className="flex gap-4 text-sm">
                            <span className="text-foreground">
                              Your answer: <span className={attempt.is_correct ? 'text-green-500 font-medium' : 'text-red-500 font-medium'}>
                                {attempt.selected_answer}
                              </span>
                            </span>
                            {!attempt.is_correct && (
                              <span className="text-foreground">
                                Correct: <span className="text-green-500 font-medium">
                                  {attempt.correct_answer}
                                </span>
                              </span>
                            )}
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            <div className="mt-8 flex gap-4 justify-center">
              <Button onClick={() => navigate('/subjects')} size="lg">
                Back to Subjects
              </Button>
              <Button 
                onClick={() => window.location.reload()} 
                variant="outline"
                size="lg"
                className="border-border"
              >
                Retake Quiz
              </Button>
            </div>
          </div>
        </div>
      </div>
    )
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <Card className="w-full max-w-2xl border-border bg-card">
          <CardContent className="p-8 text-center">
            <div className="flex flex-col items-center gap-4">
              <div className="w-12 h-12 border-4 border-primary border-t-transparent rounded-full animate-spin"></div>
              <p className="text-muted-foreground">Generating your next question with AI...</p>
              <p className="text-sm text-muted-foreground/60">This may take a few seconds</p>
            </div>
          </CardContent>
        </Card>
      </div>
    )
  }

  if (!question) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <Card className="w-full max-w-2xl border-border bg-card">
          <CardContent className="p-8 text-center">
            <p className="text-muted-foreground">No questions available</p>
          </CardContent>
        </Card>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-background py-4 sm:py-8">
      <div className="container mx-auto px-4">
        <div className="max-w-3xl mx-auto">
          <div className="mb-4 sm:mb-6 flex flex-wrap justify-between items-center gap-2 animate-slide-in">
            <div className="flex gap-2 flex-wrap">
              <span className="px-2 sm:px-3 py-1 bg-primary/10 text-primary rounded-full text-xs sm:text-sm font-medium">
                {subject}
              </span>
              <span className="px-2 sm:px-3 py-1 bg-secondary text-foreground rounded-full text-xs sm:text-sm font-medium">
                Question {questionsAnswered + 1}/{TOTAL_QUESTIONS}
              </span>
              <span className="px-2 sm:px-3 py-1 bg-accent text-foreground rounded-full text-xs sm:text-sm font-medium">
                {question.current_difficulty}
              </span>
            </div>
          </div>

          <Card className="border-border bg-card animate-scale-in hover-lift">
            <CardHeader>
              <CardTitle className="text-lg sm:text-xl text-foreground">
                <ReactMarkdown 
                  remarkPlugins={[remarkMath, remarkGfm]}
                  rehypePlugins={[rehypeKatex]}
                  className="prose prose-invert max-w-none"
                  components={{
                    p: ({node, ...props}) => <span {...props} />
                  }}
                >
                  {question.question}
                </ReactMarkdown>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-2 sm:space-y-3">
              {['A', 'B', 'C', 'D'].map((option) => {
                const optionKey = `option_${option.toLowerCase()}`
                const optionText = question[optionKey]
                
                if (!optionText) return null

                let buttonVariant = "outline"
                let extraClasses = "border-border"
                
                if (selectedAnswer === option) {
                  buttonVariant = "secondary"
                }
                
                if (showFeedback && feedback) {
                  if (option === feedback.correct_answer) {
                    extraClasses = "border-green-500 bg-green-500/10"
                  } else if (option === selectedAnswer) {
                    extraClasses = "border-red-500 bg-red-500/10"
                  }
                }

                return (
                  <Button
                    key={option}
                    variant={buttonVariant}
                    className={`w-full justify-start text-left h-auto py-2 sm:py-3 px-3 sm:px-4 ${extraClasses} transition-smooth hover:scale-102`}
                    onClick={() => !showFeedback && setSelectedAnswer(option)}
                    disabled={showFeedback}
                  >
                    <div className="flex items-start gap-2 sm:gap-3 w-full">
                      <span className="font-semibold text-sm sm:text-base flex-shrink-0">{option})</span>
                      <div className="flex-1 text-sm sm:text-base break-words overflow-wrap-anywhere">
                        <ReactMarkdown 
                          remarkPlugins={[remarkMath, remarkGfm]}
                          rehypePlugins={[rehypeKatex]}
                          className="prose prose-sm prose-invert max-w-none [&>p]:m-0 [&>code]:text-xs"
                        >
                          {optionText}
                        </ReactMarkdown>
                      </div>
                    </div>
                  </Button>
                )
              })}
            </CardContent>
          </Card>

          {!showFeedback && (
            <div className="mt-6">
              <Button
                onClick={handleSubmit}
                disabled={!selectedAnswer}
                className="w-full"
                size="lg"
              >
                Submit Answer
              </Button>
            </div>
          )}

          {showFeedback && feedback && (
            <div className="mt-6 space-y-4">
              <Card className={`border-border bg-card ${feedback.is_correct ? 'border-green-500' : 'border-red-500'}`}>
                <CardContent className="p-6">
                  <div className="flex items-center gap-3 mb-3">
                    {feedback.is_correct ? (
                      <CheckCircle2 className="w-6 h-6 text-green-500" />
                    ) : (
                      <XCircle className="w-6 h-6 text-red-500" />
                    )}
                    <span className="text-lg font-semibold text-foreground">
                      {feedback.is_correct ? 'Correct!' : 'Incorrect'}
                    </span>
                  </div>
                  <div className="text-muted-foreground mb-2 prose prose-sm prose-invert max-w-none">
                    <ReactMarkdown 
                      remarkPlugins={[remarkMath, remarkGfm]}
                      rehypePlugins={[rehypeKatex]}
                    >
                      {feedback.explanation}
                    </ReactMarkdown>
                  </div>
                  <p className="text-sm text-muted-foreground">
                    Mastery Level: {(feedback.new_mastery_level * 100).toFixed(0)}%
                  </p>
                </CardContent>
              </Card>

              <Button
                onClick={loadNextQuestion}
                className="w-full"
                size="lg"
              >
                {questionsAnswered >= TOTAL_QUESTIONS ? 'View Results' : 'Next Question'}
              </Button>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
