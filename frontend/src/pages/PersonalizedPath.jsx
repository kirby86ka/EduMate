import { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../components/ui/card'
import { Button } from '../components/ui/button'
import { ExternalLink, Sparkles, AlertCircle, Youtube, Search, BookOpen } from 'lucide-react'
import api from '../services/api'

export default function PersonalizedPath() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  
  const getRecommendations = async () => {
    setLoading(true)
    setError(null)
    try {
      const recommendations = await api.getLearningRecommendations()
      setData(recommendations)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    getRecommendations()
  }, [])
  
  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-blue-50 py-8">
        <div className="container mx-auto px-4">
          <div className="mb-8">
            <h1 className="text-4xl font-bold mb-2">Learning Recommendations</h1>
            <p className="text-muted-foreground">
              AI-powered recommendations tailored to your learning journey
            </p>
          </div>
          <div className="text-center py-12">
            <p className="text-muted-foreground">Analyzing your quiz data...</p>
          </div>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-blue-50 py-8">
        <div className="container mx-auto px-4">
          <div className="mb-8">
            <h1 className="text-4xl font-bold mb-2">Learning Recommendations</h1>
          </div>
          <Card>
            <CardContent className="p-8 text-center">
              <p className="text-red-500">{error}</p>
              <Button onClick={getRecommendations} className="mt-4">
                Try Again
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    )
  }

  if (!data || !data.has_data) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-blue-50 py-8">
        <div className="container mx-auto px-4">
          <div className="mb-8">
            <h1 className="text-4xl font-bold mb-2">Learning Recommendations</h1>
            <p className="text-muted-foreground">
              AI-powered recommendations tailored to your learning journey
            </p>
          </div>
          <Card>
            <CardContent className="p-8 text-center">
              <AlertCircle className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
              <p className="text-lg font-medium mb-2">No Quiz Data Available</p>
              <p className="text-muted-foreground mb-4">
                Complete a quiz to get personalized learning recommendations!
              </p>
              <Button onClick={() => window.location.href = '/subjects'}>
                Take a Quiz
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    )
  }
  
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-blue-50 py-8">
      <div className="container mx-auto px-4">
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2">Learning Recommendations</h1>
          <p className="text-muted-foreground">
            Based on {data.total_quizzes} quiz{data.total_quizzes !== 1 ? 'zes' : ''} and {data.total_questions} question{data.total_questions !== 1 ? 's' : ''}
          </p>
        </div>

        <div className="grid md:grid-cols-1 gap-6 mb-8">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Sparkles className="w-5 h-5 text-primary" />
                AI Recommendations
              </CardTitle>
              <CardDescription>
                Personalized insights from Gemini AI based on your quiz performance
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="p-4 bg-gradient-to-br from-purple-50 to-blue-50 rounded-lg border">
                <div className="prose prose-sm max-w-none whitespace-pre-wrap">
                  {data.ai_recommendations}
                </div>
              </div>
            </CardContent>
          </Card>

          {data.weak_areas && data.weak_areas.length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle>Areas to Focus On</CardTitle>
                <CardDescription>
                  Topics where you can improve your performance
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {data.weak_areas.map((area, index) => (
                    <div 
                      key={index}
                      className="p-4 rounded-lg border bg-white"
                    >
                      <div className="flex items-center justify-between mb-2">
                        <div>
                          <span className="font-semibold">{area.subject}</span>
                          <span className="text-muted-foreground"> • </span>
                          <span>{area.topic}</span>
                        </div>
                        <span className={`font-semibold ${
                          area.accuracy < 30 ? 'text-red-600' :
                          area.accuracy < 50 ? 'text-orange-600' :
                          'text-yellow-600'
                        }`}>
                          {area.accuracy}%
                        </span>
                      </div>
                      <p className="text-xs text-muted-foreground">
                        {area.questions_attempted} question{area.questions_attempted !== 1 ? 's' : ''} attempted
                      </p>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}

          {data.learning_resources && data.learning_resources.length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle>Learning Resources</CardTitle>
                <CardDescription>
                  Curated resources to help you improve in your weak areas
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-6">
                  {data.learning_resources.map((resource, index) => (
                    <div key={index} className="p-4 border rounded-lg bg-white">
                      <div className="mb-3">
                        <h4 className="font-semibold text-lg mb-1">{resource.title}</h4>
                        <p className="text-sm text-muted-foreground">{resource.description}</p>
                      </div>
                      <div className="flex flex-wrap gap-2">
                        <a
                          href={resource.search_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="inline-flex items-center gap-2 px-3 py-2 rounded-md border hover:bg-accent transition-colors text-sm"
                        >
                          <Search className="w-4 h-4" />
                          Google Search
                          <ExternalLink className="w-3 h-3" />
                        </a>
                        <a
                          href={resource.khan_academy_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="inline-flex items-center gap-2 px-3 py-2 rounded-md border hover:bg-accent transition-colors text-sm"
                        >
                          <BookOpen className="w-4 h-4" />
                          Khan Academy
                          <ExternalLink className="w-3 h-3" />
                        </a>
                        <a
                          href={resource.youtube_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="inline-flex items-center gap-2 px-3 py-2 rounded-md border hover:bg-accent transition-colors text-sm"
                        >
                          <Youtube className="w-4 h-4" />
                          YouTube
                          <ExternalLink className="w-3 h-3" />
                        </a>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}
        </div>

        <div className="text-center">
          <Button onClick={getRecommendations} variant="outline">
            <Sparkles className="w-4 h-4 mr-2" />
            Refresh Recommendations
          </Button>
        </div>
      </div>
    </div>
  )
}
